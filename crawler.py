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
        
        # Playwright 인스턴스를 클래스 속성으로 저장
        self.playwright = sync_playwright().start()
        # 브라우저 인스턴스 생성
        self.browser = self.playwright.chromium.launch(**self.setBrowserOption())
        

        self.crawl_data = self.siteDivision()

    
    def __del__(self):
        # 객체가 삭제될 때 정리
        if hasattr(self, 'browser') and self.browser:
            self.browser.close()
        if hasattr(self, 'playwright') and self.playwright:
            self.playwright.stop()
        
    # 수집하는 사이트 출력
    @staticmethod
    def printSite(site):
        print(f"Crawling Site : {site}")
    
    # playwright 브라우저 옵션 설정
    def setBrowserOption(self):
        return {
            'headless': False   # headless=True로 설정하면 브라우저가 보이지 않음
        }
        
        
    ## 메인화면에서 URL 리스트 파싱
    def parseCrawlUrl(self, main_url):
        page = self.browser.new_page()
        
        # 페이지 로드
        page.goto(main_url)
        
        # SOURCE._contents에 해당하는 모든 요소 선택
        tbody_elements = page.locator(self.SOURCE._contents).all()
        
        tr_elements = tbody_elements[0].locator('tr').all()
        
        crawl_url_list = []
        
        if(self.SOURCE._site == 'dc'):
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
        
        return crawl_url_list

    def getCrawlUrl(self):

            # 실제로 수집해야할 URL 리스트
            crawl_url_list = []
            
            type = self.SOURCE._type
            
            main_url = ''
            
            type_list = type.split('/')
            
            link_type = type_list[0]
            parameter_type = type_list[1]
            
            for i in range(int(self.SOURCE._min_parameter), int(self.SOURCE._max_parameter)):
                
                if(link_type == 'parameter'):
                    main_url = self.SOURCE._url + '&' if '?' in self.SOURCE._url else self.SOURCE._url + '?'
                
                # 메인화면에서 수집해야할 URL 리스트
                link_url_list = []
                
                main_url += f'{self.SOURCE._parameter}={str(i)}'
                
                if(parameter_type == 'page'):
                    link_url_list = self.parseCrawlUrl(main_url)
                    if(len(link_url_list) > 0):
                        crawl_url_list.extend(link_url_list)
                        
                elif(parameter_type == 'result'):
                    crawl_url_list.append(main_url)
                 
                if self.ARGV._test:
                    break
                  
                print(f"Link URL List : {link_url_list}")
                
            print(f"Crawl URL List : {crawl_url_list}")
                 
    
                    
            if(len(crawl_url_list) < 0):
                print("Error: No crawl url found")
                sys.exit(1)
                
            return crawl_url_list
                    
            

    # 사이트 구분
    def siteDivision(self):
        
        crawl_data = []
        url_list = []
        
        if(self.SOURCE._site == 'dc'):
            self.printSite(self.SOURCE._site)
            url_list = self.getCrawlUrl()
            crawl_data = self.mainCrawler(url_list)
        
        return crawl_data


    def mainCrawler(self, crawl_url_list):
        print(f"Crawling URL : {crawl_url_list}")
        print(f"Crawling URL Count : {len(crawl_url_list)}")
        
        crawl_data = []
        page = self.browser.new_page()

        for url in crawl_url_list:
            
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
                
        return crawl_data
    
    def getCrawlData(self):
        return self.crawl_data
    
        
