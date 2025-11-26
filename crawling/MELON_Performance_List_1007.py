import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------------------------------
# 1. 설정 및 드라이버 초기화
# ----------------------------------------------------

# 멜론티켓 글로벌 페이지 URL
URL = "https://tkglobal.melon.com/main/index.htm?langCd=EN"

try:
    # Chrome WebDriver 자동 설치 및 설정
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except Exception as e:
    print(f"WebDriver 초기화 오류: {e}")
    print("Chrome 드라이버를 확인해 주세요.")
    exit()

# ----------------------------------------------------
# 2. 웹 페이지 접속 및 데이터 수집
# ----------------------------------------------------
try:
    print(f"URL 접속 시도: {URL}")
    driver.get(URL)
    
    # 페이지가 완전히 로딩될 때까지 대기 (첫 번째 리스트 아이템이 나타날 때까지 기다립니다)
    wait = WebDriverWait(driver, 15)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#conts > div > div:nth-child(1) > ul > li:nth-child(1)"))
    )
    print("페이지 로딩 완료. 데이터 수집 시작.")

    # 기본 경로 (UL 태그)
    list_base_xpath = "#conts > div > div:nth-child(1) > ul > li"
    
    # 리스트 전체 항목 찾기
    performance_list = driver.find_elements(By.CSS_SELECTOR, list_base_xpath)
    
    if not performance_list:
        print("공연 리스트를 찾을 수 없거나 리스트가 비어 있습니다.")
    else:
        print(f"총 {len(performance_list)}개의 공연 항목을 찾았습니다.\n")
        
        # 반복문을 사용하여 모든 공연 정보를 추출
        for i, item in enumerate(performance_list):
            
            # 리스트 아이템의 CSS 선택자를 재구성 (i+1 번째 항목)
            base_selector = f"#conts > div > div:nth-child(1) > ul > li:nth-child({i+1})"
            
            # --- 개별 데이터 추출 ---
            try:
                # 1. 이미지 URL
                img_selector = f"{base_selector} > div.thumb_180x254 > img"
                img_element = driver.find_element(By.CSS_SELECTOR, img_selector)
                image_url = img_element.get_attribute('src')
                
                # 2. 축제/공연 이름 (Title)
                title_selector = f"{base_selector} > div.article > h2"
                title = driver.find_element(By.CSS_SELECTOR, title_selector).text
                
                # 3. 축제 날짜 (Date)
                date_selector = f"{base_selector} > div.article > dl > dd:nth-child(2)"
                date = driver.find_element(By.CSS_SELECTOR, date_selector).text
                
                # 4. 축제 장소 (Location)
                location_selector = f"{base_selector} > div.article > dl > dd:nth-child(4)"
                location = driver.find_element(By.CSS_SELECTOR, location_selector).text
                
                # 5. 축제 장르 (Genre)
                genre_selector = f"{base_selector} > div.article > dl > dd:nth-child(6)"
                genre = driver.find_element(By.CSS_SELECTOR, genre_selector).text
                
                # 6. 관람 연령 (Age Limit)
                age_selector = f"{base_selector} > div.article > dl > dd:nth-child(8)"
                age_limit = driver.find_element(By.CSS_SELECTOR, age_selector).text
                
                # --- 결과 출력 ---
                print(f"[{i+1}번째 공연 정보]")
                print(f"  제목: {title}")
                print(f"  날짜: {date}")
                print(f"  장소: {location}")
                print(f"  장르: {genre}")
                print(f"  연령: {age_limit}")
                print(f"  이미지 URL: {image_url}")
                print("-" * 30)

            except Exception as item_e:
                print(f"⚠️ {i+1}번째 항목 크롤링 중 오류 발생. (해당 항목 건너뛰기)")
                print(f"오류 내용: {item_e}")
                print("-" * 30)
                continue

except Exception as e:
    print(f"\n❌ 크롤링 중 심각한 오류 발생: {e}")

finally:
    # 드라이버 종료
    driver.quit()
    print("\n✅ 웹 드라이버 종료 및 크롤링 완료.")