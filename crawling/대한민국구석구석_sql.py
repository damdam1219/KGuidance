import re
import time
import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------------------------------
# 1. MySQL 연결
# ----------------------------------------------------
def connect_mysql():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="performance",
        charset="utf8mb4"
    )

# ----------------------------------------------------
# 2. 테이블 생성
# ----------------------------------------------------
def create_tables():
    conn = connect_mysql()
    cursor = conn.cursor()
    
    # korea_perform 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS korea_perform (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filter_type VARCHAR(5),
            title VARCHAR(255),
            start_date VARCHAR(20),
            end_date VARCHAR(20),
            image_url TEXT,
            instagram_url TEXT,
            address TEXT,
            latitude DOUBLE,
            longitude DOUBLE,
            description TEXT,
            detail_url TEXT
        ) CHARACTER SET utf8mb4;
    """)
    
    # 좌표 실패 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS korea_location_fail (
            id INT AUTO_INCREMENT PRIMARY KEY,
            perform_id INT,  -- korea_perform id와 연결
            filter_type VARCHAR(5),
            title VARCHAR(255),
            start_date VARCHAR(20),
            end_date VARCHAR(20),
            image_url TEXT,
            instagram_url TEXT,
            address TEXT,
            description TEXT,
            detail_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (perform_id) REFERENCES korea_perform(id) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4;
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 테이블 확인/생성 완료")

# ----------------------------------------------------
# 3. 카카오 지오코딩
# ----------------------------------------------------
KAKAO_API_KEY = "c13a73b79a2071caa99bc2f339a7974b"

def geocode_address(address):
    if not address or address == "N/A":
        return None, None
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        params = {"query": address}
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        if result.get("documents"):
            lat = float(result["documents"][0]["y"])
            lon = float(result["documents"][0]["x"])
            return lat, lon
        return None, None
    except Exception as e:
        print(f"⚠️ 지오코딩 실패 ({address}): {e}")
        return None, None

# ----------------------------------------------------
# 4. 날짜 전처리
# ----------------------------------------------------
def preprocess_date(date_string):
    dates = re.findall(r'(\d{4}\.\d{2}\.\d{2})', date_string)
    start_date = dates[0] if dates else None
    end_date = dates[-1] if dates else None
    return start_date, end_date

# ----------------------------------------------------
# 5. 상세 페이지 크롤링
# ----------------------------------------------------
def crawl_festival_detail(detail_url):
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    data = {'description': "N/A", 'address': "N/A", 'instagram_url': "N/A"}

    try:
        driver.get(detail_url)
        SELECTORS = {
            'description': "#mainTab > div > div > section.poster_detail > div > div.poster_info_content > div.m_img_fst",
            'address': "#mainTab > div > div > section.poster_detail > div > div.poster_detail_wrap > div > div.img_info_box > ul > li:nth-child(2) > p",
            'instagram_url': "#mainTab > div > div > section.poster_detail > div > div.poster_detail_wrap > div > div.img_info_box > ul > li:nth-child(6) > a"
        }

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['description'])))

        try:
            data['description'] = re.sub(r'\s+', ' ', driver.find_element(By.CSS_SELECTOR, SELECTORS['description']).text.strip())
        except: pass
        try:
            data['address'] = driver.find_element(By.CSS_SELECTOR, SELECTORS['address']).text.strip()
        except: pass
        try:
            data['instagram_url'] = driver.find_element(By.CSS_SELECTOR, SELECTORS['instagram_url']).get_attribute('href')
        except: pass

    except Exception as e:
        print(f"❌ 상세 페이지 크롤링 실패: {e}")
    finally:
        driver.quit()
    return data

# ----------------------------------------------------
# 6. 메인 크롤링
# ----------------------------------------------------
def get_all_festival_data():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)

    results = []

    try:
        driver.get("https://korean.visitkorea.or.kr/kfes/list/wntyFstvlList.do")
        print("✅ 기본 페이지 접속 완료")
        Select(driver.find_element(By.ID, "searchArea")).select_by_value("1")  # 서울
        time.sleep(1)

        for date_filter in ['A', 'B']:
            Select(driver.find_element(By.ID, "searchDate")).select_by_value(date_filter)
            time.sleep(1)
            search_button = driver.find_element(By.CSS_SELECTOR, "button.btn_search")
            driver.execute_script("arguments[0].click();", search_button)
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#fstvlList > li")))
            except:
                print(f"⚠️ '{date_filter}' 결과 없음")
                continue
            time.sleep(2)

            page = 1
            while True:
                items = driver.find_elements(By.CSS_SELECTOR, "#fstvlList > li")
                if not items: break

                for idx, item in enumerate(items, start=1):
                    try:
                        title = item.find_element(By.CSS_SELECTOR, "a > div.other_festival_content > strong").text.strip()
                        date_raw = item.find_element(By.CSS_SELECTOR, "a > div.other_festival_content > div.date").text
                        start_date, end_date = preprocess_date(date_raw)
                        img_url = item.find_element(By.CSS_SELECTOR, "a > div.other_festival_img > img").get_attribute('src')
                        detail_url = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                        detail_data = crawl_festival_detail(detail_url)

                        lat, lon = geocode_address(detail_data['address'])
                        print(f"📍 {title} → 위도:{lat}, 경도:{lon}")

                        results.append({
                            'filter_type': date_filter,
                            'title': title,
                            'start_date': start_date,
                            'end_date': end_date,
                            'image_url': img_url,
                            'instagram_url': detail_data['instagram_url'],
                            'address': detail_data['address'],
                            'latitude': lat,
                            'longitude': lon,
                            'description': detail_data['description'],
                            'detail_url': detail_url
                        })

                    except Exception as e:
                        print(f"❌ {idx}번째 축제 오류: {e}")

                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, "div.paging_wrap a.next")
                    if "disabled" in next_btn.get_attribute("class"):
                        break
                    driver.execute_script("arguments[0].click();", next_btn)
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#fstvlList > li")))
                    page += 1
                    time.sleep(1)
                except: break

    except Exception as e:
        print(f"❌ 메인 실행 오류: {e}")
    finally:
        driver.quit()

    print(f"\n🎉 총 {len(results)}개 축제 크롤링 완료")
    return results

# ----------------------------------------------------
# 7. MySQL 저장
# ----------------------------------------------------
def save_festivals_with_fail(data):
    if not data: return
    conn = connect_mysql()
    cursor = conn.cursor()
    fail_entries = []

    for d in data:
        # korea_perform에 저장
        cursor.execute("""
            INSERT INTO korea_perform (
                filter_type, title, start_date, end_date, image_url,
                instagram_url, address, latitude, longitude, description, detail_url
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            d['filter_type'], d['title'], d['start_date'], d['end_date'],
            d['image_url'], d['instagram_url'], d['address'],
            d['latitude'], d['longitude'], d['description'], d['detail_url']
        ))
        perform_id = cursor.lastrowid

        # 좌표가 없는 경우 korea_location_fail에 저장
        if d['latitude'] is None or d['longitude'] is None:
            fail_entries.append((perform_id, d['filter_type'], d['title'], d['start_date'], d['end_date'],
                                 d['image_url'], d['instagram_url'], d['address'], d['description'], d['detail_url']))

    if fail_entries:
        cursor.executemany("""
            INSERT INTO korea_location_fail (
                perform_id, filter_type, title, start_date, end_date, image_url,
                instagram_url, address, description, detail_url
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, fail_entries)

    conn.commit()
    print(f"💾 {len(data)}개 데이터 korea_perform 저장 완료, {len(fail_entries)}개 좌표 실패 데이터 korea_location_fail 저장 완료")
    cursor.close()
    conn.close()

# ----------------------------------------------------
# 8. 실행
# ----------------------------------------------------
if __name__ == "__main__":
    create_tables()
    festival_data = get_all_festival_data()
    save_festivals_with_fail(festival_data)
