import sys
from playwright.sync_api import sync_playwright

from configData import get_argv, get_source
from custom import get_number_custom
from toJson import save_data_to_json

class Crawler:
    ARGV = None
    SOURCE = None

    def __init__(self):
        self.ARGV = get_argv()
        self.SOURCE = get_source()
        
        print(f"Crawling {self.SOURCE._site} URL : {self.SOURCE._url}")
        
        
    @staticmethod
    def print_site(site):
        print(f"Crawling Site : {site}")
    
    def set_browser_option(self):
        
        # headless=True로 설정하면 브라우저가 보이지 않음
        return {
            'headless': False
        }

    def dc_crawl(self):
        # Playwright 실행
        with sync_playwright() as p:
            # Chromium 브라우저 열기
            browser = p.chromium.launch(**self.set_browser_option())  ## **은 언패킹 연산자 -> 딕셔너리를 키워드로 풀어서 전달함
            page = browser.new_page()
            
            type = self.SOURCE._type
            
            
            # 페이지 로드
            page.goto(self.SOURCE._url)
            
            # SOURCE._contents에 해당하는 모든 요소 선택
            tbody_elements = page.locator(self.SOURCE._contents).all()
            
            tr_elements = tbody_elements[0].locator('tr').all()
            
            crawl_url_list = []
            
            # 각 요소의 href 속성 가져오기
            for element in tr_elements:
                try:
                    if('us-post' in element.get_attribute('class')):
                        title_element = element.locator('.gall_tit').first
                        a_element = title_element.locator('a').first
                        
                        crawl_url_list.append(self.SOURCE._host + a_element.get_attribute('href'))

                except Exception as e:
                    print(f"Error getting href: {e}")
            
            page.close()
            
            if(len(crawl_url_list) > 0):
                return self.main_crawl(browser, crawl_url_list)
            else:
                print("Error: No crawl url found")
                
                sys.exit(1)

    # 사이트 구분
    def crawl_site_division(self):
        
        crawl_data = []
        
        if(self.SOURCE._site == 'dc'):
            self.print_site(self.SOURCE._site)
            crawl_data = self.dc_crawl()
        
        return crawl_data


    def main_crawl(self, browser, crawl_url_list):
        print(f"Crawling URL : {crawl_url_list}")
        print(f"Crawling URL Count : {len(crawl_url_list)}")
        
        crawl_data = []

        for url in crawl_url_list:
            page = browser.new_page()
            page.goto(url)
            
            if(page.url == url):
                
                # 게시물 정보 가져오기
                subject_text = page.locator(self.SOURCE._subject['selector']).first.text_content()
                
                # script 태그 제거 후 콘텐츠 가져오기
                content_element = page.evaluate("""
                    selector => {
                        const element = document.querySelector(selector);
                        const scripts = element.getElementsByTagName('script');
                        while(scripts.length > 0){
                            scripts[0].parentNode.removeChild(scripts[0]);
                        }
                        return element.textContent;
                    }
                """, self.SOURCE._content['selector'])
                
                content_text = content_element.replace('\n', '').replace('\t', '').replace('\r', '').replace('\v', '').replace('\f', '')
                
                date_text = get_number_custom(page.locator(self.SOURCE._date['selector']).first.text_content())
                view_text = get_number_custom(page.locator(self.SOURCE._view['selector']).first.text_content())
                like_text = get_number_custom(page.locator(self.SOURCE._like['selector']).first.text_content())

                crawl_data.append({
                    'subject': subject_text,
                    'content': content_text,
                    'date': date_text,
                    'view': view_text,
                    'like': like_text,
                    'url': url
                })
                
                if self.ARGV._test:
                    break
                
            else:
                print(f"Error: {page.url} is not {url}")
            
            page.close()
                
        return crawl_data
    
    def start_crawl(self):
        crawl_data = self.crawl_site_division()
        
        
        return crawl_data
