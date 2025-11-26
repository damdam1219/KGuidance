import time
import csv
import re
from urllib.parse import urljoin

# Selenium 및 관련 모듈 임포트
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# --- 설정 정보 ---
BASE_URL = "https://english.visitseoul.net"
LIST_PAGE_URL_FORMAT = BASE_URL + "/entertainment?curPage={}"
OUTPUT_FILE = "visitseoul_dt_dd_final_stable_ver2.csv"

# ⚠️ 암묵적/명시적 대기 시간 설정 (정보 로드 시간 확보)
IMPLICIT_WAIT_TIME = 30
EXPLICIT_WAIT_TIME = 30

# 수집할 상세 정보의 dt 제목 목록 (DT의 텍스트가 이 문자열로 시작하는지 확인)
TARGET_DT_FIELDS = {
    'Hours of Operation': None,
    'Important': None,
    'Fee': None,
    # CSV 헤더에 address, transportation이 소문자이므로, 
    # dt 텍스트 매칭용으로 대문자 시작 키를 사용합니다.
    'Address': None,      
    'Transportation': None 
}

## 📚 상세 페이지 크롤링 함수 (DT/DD 기반 파싱)
def crawl_detail_page(driver, detail_url):
    full_url = urljoin(BASE_URL, detail_url)
    print(f"  -> 상세 페이지 Selenium 크롤링 중: {full_url}")
    
    DESCRIPTION_SELECTOR = "#container > div.wide-inner > div.text-area p"
    DETAIL_CONTAINER_SELECTOR = "#container > div.detial-cont-element.active > div"
    
    # 결과를 저장할 딕셔너리 초기화 (DT 매칭용)
    result_data = {k: None for k in TARGET_DT_FIELDS} 
    
    try:
        # 1. 상세 페이지 로드 및 대기
        driver.get(full_url)
        WebDriverWait(driver, EXPLICIT_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, DESCRIPTION_SELECTOR))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    except Exception as e:
        print(f"  ❌ 상세 페이지 로드/대기 오류: {e}")
        # 오류 발생 시 CSV 헤더에 맞는 키로 None 값을 반환
        return {
            'description': "로드 오류/시간 초과",
            'address': None, 'transportation': None,
            'image_urls': "", 'image_count': 0,
            'Hours of Operation': None, 'Important': None, 'Fee': None
        }

    # --- 1. description 추출 ---
    description_tag = soup.select_one(DESCRIPTION_SELECTOR)
    description = description_tag.text.strip() if description_tag else None
    
    # --- 2. dt/dd 기반 필드 추출 ---
    detail_container = soup.select_one(DETAIL_CONTAINER_SELECTOR)
    if detail_container:
        dl_items = detail_container.find_all('dl')
        
        for dl in dl_items:
            dt_tag = dl.find('dt')
            dd_tag = dl.find('dd')
            
            if dt_tag and dd_tag:
                dt_text = dt_tag.text.strip()
                dd_text = dd_tag.text.strip()
                
                for target_field in TARGET_DT_FIELDS.keys():
                    if dt_text.startswith(target_field):
                        result_data[target_field] = dd_text
                        break

    # --- 3. Image URLs 추출 ---
    image_urls_list = []
    image_items = soup.select("#container .wide-slide-element .owl-stage .owl-item > div")
    
    for item in image_items:
        style = item.get('style')
        if style:
            match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
            if match:
                image_url = urljoin(BASE_URL, match.group(1).strip())
                image_urls_list.append(image_url)

    unique_image_urls = sorted(list(set(image_urls_list)))
    image_urls = " | ".join(unique_image_urls)
    image_count = len(unique_image_urls)
    
    time.sleep(2) 
    
    # 🚨 수정된 부분: CSV 헤더에 정의된 정확한 키(address, transportation)로 반환
    return {
        'description': description,
        # CSV 헤더에 정의된 소문자 키로 값을 할당합니다.
        'address': result_data.get('Address'), 
        'transportation': result_data.get('Transportation'),
        'image_urls': image_urls,
        'image_count': image_count,
        
        # 나머지 3개 필드는 키가 CSV 헤더와 일치합니다.
        'Hours of Operation': result_data.get('Hours of Operation'),
        'Important': result_data.get('Important'),
        'Fee': result_data.get('Fee')
    }

## 🚀 메인 크롤링 함수
def main_crawler():
    page_num = 1
    # 🚨 최종 CSV 헤더 목록 정의 (10개 필드)
    fieldnames = [
        'title', 'url', 'description', 'address', 'transportation', 
        'image_urls', 'image_count', 'Hours of Operation', 'Important', 'Fee'
    ]
    
    try:
        options = Options()
        options.add_argument('headless') 
        options.add_argument('disable-gpu')
        options.add_argument('lang=en_US') 
        
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(IMPLICIT_WAIT_TIME)
    except Exception as e:
        print("❌ Selenium WebDriver 초기화 실패. ChromeDriver를 확인하세요.")
        print(f"오류 내용: {e}")
        return

    print(f"======================================")
    print(f"🔍 비짓서울(Visit Seoul) 크롤링 시작...")
    print(f"======================================")

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        while True:
            list_page_url = LIST_PAGE_URL_FORMAT.format(page_num)
            print(f"\n--- 🌐 {page_num} 페이지 항목 목록 로딩 중 ---")
            
            try:
                driver.get(list_page_url)
                WebDriverWait(driver, EXPLICIT_WAIT_TIME).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#postSearchFrm > section > div.article-list-slide > ul > li"))
                )
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')

            except Exception:
                print("✅ 마지막 페이지에 도달했거나 목록 로드 오류가 발생했습니다. 크롤링을 종료합니다.")
                break
            
            list_items = soup.select("#postSearchFrm > section > div.article-list-slide > ul > li")
            
            if not list_items:
                print("✅ 더 이상 항목이 없습니다. 크롤링을 종료합니다.")
                break
            
            for item in list_items:
                title_tag = item.select_one("a > div.infor-element > div > span.title")
                title = title_tag.text.strip() if title_tag else "제목 없음"
                
                url_tag = item.select_one("a")
                detail_url = url_tag.get('href') if url_tag else None
                
                if detail_url and title != "제목 없음": 
                    detail_data = crawl_detail_page(driver, detail_url)
                    
                    # 🚨 final_data는 fieldnames의 10개 키만 포함하도록 보장됩니다.
                    final_data = {
                        'title': title,
                        'url': urljoin(BASE_URL, detail_url),
                        **detail_data 
                    }
                    writer.writerow(final_data)
                
            page_num += 1
            time.sleep(5) 

    driver.quit()
    print(f"\n======================================")
    print(f"🎉 크롤링이 성공적으로 완료되었습니다.")
    print(f"======================================")

if __name__ == "__main__":
    main_crawler()