import time
import re
import pandas as pd
import mysql.connector
import requests 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mysql.connector import errorcode

# Google Maps API 라이브러리 추가
import googlemaps

# ----------------------------------------------------
# 1. DB 설정 및 크롤링 설정
# ----------------------------------------------------

# !!! 사용자 정보를 자신의 MySQL 설정에 맞게 변경하세요 !!!
DB_CONFIG = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'performance'
}
TABLE_NAME = 'MELON_perfor'
URL = "https://tkglobal.melon.com/main/index.htm?langCd=EN"

# ----------------------------------------------------
# !!! Google API 설정 (Maps Platform Key를 발급받아 여기에 입력하세요) !!!
# ----------------------------------------------------
# 보안을 위해 실제 키는 환경 변수 등으로 관리하는 것이 좋습니다.
GOOGLE_MAPS_API_KEY = "." 
try:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except Exception:
    gmaps = None


# ----------------------------------------------------
# 2. DB 연결 및 테이블 생성 함수 (address, latitude, longitude 컬럼 추가/수정)
# ----------------------------------------------------

def setup_database(db_config, table_name):
    """DB에 연결하고 필요한 데이터베이스 및 테이블을 생성합니다."""
    try:
        conn = mysql.connector.connect(
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host']
        )
        cursor = conn.cursor()

        DB_NAME = db_config['database']
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
            print(f"✅ 데이터베이스 '{DB_NAME}' 확인 또는 생성 완료.")
            conn.database = DB_NAME
        except mysql.connector.Error as err:
            print(f"데이터베이스 오류: {err}")
            return None, None

        # 테이블 생성: address(주소), latitude(위도), longitude(경도) 컬럼 추가
        TABLE_SCHEMA = (f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                start_date DATE,
                end_date DATE,
                location VARCHAR(255),
                address VARCHAR(512),  
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                genre VARCHAR(100),
                age_limit VARCHAR(50),
                image_url TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cursor.execute(TABLE_SCHEMA)
        print(f"✅ 테이블 '{table_name}' 확인 또는 생성 완료.")
        return conn, cursor

    except mysql.connector.Error as err:
        print(f"❌ DB 연결 실패: {err}")
        return None, None

# ----------------------------------------------------
# 3. 데이터 전처리 및 지오코딩 함수
# ----------------------------------------------------

def preprocess_date(date_string):
    """날짜 문자열을 시작일과 종료일로 분리하고 DATE 형식으로 변환합니다."""
    start_date = None
    end_date = None
    dates = re.findall(r'(\d{4}\.\d{2}\.\d{2})', date_string)
    
    if len(dates) >= 1:
        start_date = dates[0].replace('.', '-')
        end_date = dates[0].replace('.', '-')
        if len(dates) == 2:
            end_date = dates[1].replace('.', '-')
            
    return start_date, end_date

def geocode_location_google(location_name):
    """Google Geocoding API를 사용하여 장소 이름에서 주소, 위도, 경도를 추출합니다."""
    
    if not gmaps:
        print("  ❌ Google Maps Client가 초기화되지 않았습니다. API 키를 확인하세요.")
        return None, None, None

    try:
        # 🚨 한국으로 검색 범위를 명시적으로 제한
        geocode_result = gmaps.geocode(
            location_name, 
            language='ko',
            components={'country': 'kr'}  # <--- 이 옵션이 검색 결과를 한국으로 제한합니다.
        ) 
        
        if geocode_result:
            result = geocode_result[0]
            
            # 주소
            address = result['formatted_address']
            
            # 좌표
            location = result['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            
            print(f"  ✅ 지오코딩 성공: {address}")
            return address, latitude, longitude
        else:
            print(f"  ⚠️ 지오코딩 결과 없음: {location_name}")
            return None, None, None
            
    except Exception as e:
        print(f"  ❌ Google Geocoding API 호출 오류 발생: {e}")
        return None, None, None

# ----------------------------------------------------
# 4. 메인 크롤링 및 적재 로직
# ----------------------------------------------------

def run_crawler_and_load_db():
    conn, cursor = setup_database(DB_CONFIG, TABLE_NAME)
    if not conn:
        return

    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(URL)
        
        wait = WebDriverWait(driver, 15)
        list_selector = "#conts > div > div:nth-child(1) > ul > li"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, list_selector)))

        performance_list = driver.find_elements(By.CSS_SELECTOR, list_selector)
        print(f"\n총 {len(performance_list)}개의 공연 항목 발견.")

        for i, item in enumerate(performance_list):
            base_selector = f"#conts > div > div:nth-child(1) > ul > li:nth-child({i+1})"
            
            try:
                # 1. 크롤링 데이터 추출
                image_url = driver.find_element(By.CSS_SELECTOR, f"{base_selector} > div.thumb_180x254 > img").get_attribute('src')
                title = driver.find_element(By.CSS_SELECTOR, f"{base_selector} > div.article > h2").text
                date_raw = driver.find_element(By.CSS_SELECTOR, f"{base_selector} > div.article > dl > dd:nth-child(2)").text
                
                # location에 크롤링된 영문 장소명이 담김
                location = driver.find_element(By.CSS_SELECTOR, f"{base_selector} > div.article > dl > dd:nth-child(4)").text
                
                genre = driver.find_element(By.CSS_SELECTOR, f"{base_selector} > div.article > dl > dd:nth-child(6)").text
                age_limit = driver.find_element(By.CSS_SELECTOR, f"{base_selector} > div.article > dl > dd:nth-child(8)").text

                # 2. 데이터 전처리 (날짜)
                start_date, end_date = preprocess_date(date_raw)
                if not start_date: continue

                # 3. 지오코딩 쿼리 강화 및 실행 (수정된 부분)
                
                # 3-1. 특수 문자 제거: 슬래시(/), 쉼표(,), 마침표(.)를 공백으로 대체하고 앞뒤 공백 제거
                cleaned_location = location.replace('/', ' ').replace(',', ' ').replace('.', '').strip()
                
                # 3-2. 지오코딩 쿼리에 'South Korea'를 추가하여 검색어 강화
                search_query = cleaned_location + ", South Korea"
                print(f"  🔍 지오코딩 쿼리: {search_query}") 
                
                # 3-3. Google Geocoding API 호출
                address, latitude, longitude = geocode_location_google(search_query)
                
                # 4. DB 적재 (address, latitude, longitude 필드 추가)
                insert_query = f"""
                    INSERT INTO {TABLE_NAME} 
                    (title, start_date, end_date, location, address, latitude, longitude, genre, age_limit, image_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (title, start_date, end_date, location, address, latitude, longitude, genre, age_limit, image_url)
                
                cursor.execute(insert_query, data)
                print(f"  ✅ {i+1}번째 공연 적재 완료: {title}")

            except Exception as item_e:
                print(f"  ❌ {i+1}번째 항목 처리 중 오류 발생. (오류: {item_e})")
                continue

        conn.commit()
        print("\n🎉 모든 데이터 DB에 최종 커밋 완료.")

    except Exception as e:
        print(f"\n🛑 메인 실행 중 심각한 오류 발생: {e}")

    finally:
        if 'driver' in locals(): driver.quit()
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("DB 연결 종료.")
            
if __name__ == "__main__":
    run_crawler_and_load_db()