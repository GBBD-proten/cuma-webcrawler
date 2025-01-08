from argv import ArgvData
from source import SourceData

from playwright.sync_api import sync_playwright

ARGV = None
SOURCE = None

def set_data():
    global ARGV, SOURCE
    
    ARGV = ArgvData.get_instance()
    SOURCE = SourceData(ARGV._id)

def dc_crawl():
    # Playwright 실행
    with sync_playwright() as p:
        # Chromium 브라우저 열기
        browser = p.chromium.launch(headless=False)  # headless=True로 설정하면 브라우저가 보이지 않음
        page = browser.new_page()
        
        # 페이지 로드
        page.goto(SOURCE._url)
        
        # SOURCE._contents에 해당하는 모든 요소 선택
        tbody_elements = page.locator(SOURCE._contents).all()
        
        tr_elements = tbody_elements[0].locator('tr').all()
        
        # 각 요소의 href 속성 가져오기
        for element in tr_elements:
            print(element.get_attribute('class'))
            try:
                if(element.get_attribute('class') in 'us-post'):
                    print(element.locator('a').get_attribute('href'))
                
            except Exception as e:
                print(f"Error getting href: {e}")
        
        # 브라우저 닫기
        browser.close()

def main_crawl():
    set_data()
    
    print(f"Crawling URL : {SOURCE._url}")
    
    if(SOURCE._site == 'dc'):
        print(f"Crawling Site : {SOURCE._site}")
        dc_crawl()

   
    
