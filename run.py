import sys

from configData import setConfig, getArgv
from crawler import Crawler
from toJson import saveJson
from toElasticsearch import toElasticsearch

argv = None

def modeDivision():
    global argv
    argv = getArgv()
    
    if argv._mode == "cra":
        crawler = Crawler()
        crawl_data = crawler.getCrawlData()
        crawl_data_count = len(crawl_data)
        
        print(f"Crawl Data Count : {crawl_data_count}")
        
        if crawl_data_count > 0:
            
            if argv._json:
                saveJson(crawl_data)

            if argv._bulk:  
                # elasticsearch 색인
                to_elasticsearch = toElasticsearch()
                isOk = to_elasticsearch.toElasticsearch()
                to_elasticsearch.closeElasticsearch()

                if isOk:
                    return True
                else:
                    return False
        else:
            print("[INFO] No crawl data found")
            return True
        
    elif argv._mode == "index":
        to_elasticsearch = toElasticsearch()
        to_elasticsearch.createIndex()
        to_elasticsearch.closeElasticsearch()

def main():
    if len(sys.argv) <= 2:
        print("Error: ID parameter is required", file=sys.stderr)
        print("Error: Check parameter -python run.py <id> <mode> <option>", file=sys.stderr)
        sys.exit(1)  # 1은 에러 코드를 나타냄 (0은 정상 종료)
        
    # data 설정
    setConfig(sys.argv)
    
    # 모드 구분
    isOk = modeDivision()  
    
    if isOk:
        print(f"[INFO] Crawler {argv._id} Mode : {argv._mode} Success")
    else:
        print(f"[ERROR] Crawler {argv._id} Mode : {argv._mode} Failed")
        
if __name__ == "__main__":
    main()