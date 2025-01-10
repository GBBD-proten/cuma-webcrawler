import sys

from configData import set_config, get_argv
from crawler import Crawler
from toJson import save_data_to_json
from toElasticsearch import toElasticsearch

argv = None

def mode_division():
    global argv
    argv = get_argv()
    
    if argv._mode == "cra":
        crawler = Crawler()
        crawl_data = crawler.start_crawl()
        crawl_data_count = len(crawl_data)
        
        print(f"Crawl Data Count : {crawl_data_count}")
        
        if crawl_data_count > 0:
            if argv._json:
                save_data_to_json(crawl_data)
                
                return True
            
            save_data_to_json(crawl_data)
            
            # elasticsearch 색인
            toelasticsearch = toElasticsearch()
            isOk = toelasticsearch.to_elasticsearch()
            
            if isOk:
                return True
            else:
                return False
        else:
            print("[INFO] No crawl data found")
            return True
        
    elif argv._mode == "index":
        toelasticsearch = toElasticsearch()
        toelasticsearch.create_index()


def main():
    if len(sys.argv) <= 2:
        print("Error: ID parameter is required", file=sys.stderr)
        print("Error: Check parameter -python run.py <id> <mode> <option>", file=sys.stderr)
        sys.exit(1)  # 1은 에러 코드를 나타냄 (0은 정상 종료)
        
    # data 설정
    set_config(sys.argv)
    
    # 모드 구분
    isOk = mode_division()  
    
    if isOk:
        print(f"[INFO] Crawler {argv._id} Mode : {argv._mode} Success")
    else:
        print(f"[ERROR] Crawler {argv._id} Mode : {argv._mode} Failed")
        
if __name__ == "__main__":
    main()