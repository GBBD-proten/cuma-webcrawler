import sys

from configData import set_config, get_argv
from crawler import crawl_site_division
from toJson import save_data_to_json
from toElasticsearch import to_elasticsearch, create_index



def mode_division():
    argv = get_argv()
    
    if argv._mode == "cra":
        crawl_data = crawl_site_division()
        
        # json 저장
        save_data_to_json(crawl_data)
        
        # elasticsearch 색인
        isOk = to_elasticsearch()
        
        if isOk:
            print(f"Crawl Data Index Success")
        else:
            print(f"Crawl Data Index Failed")
        
    elif argv._mode == "index":
        create_index()


def main():
    if len(sys.argv) <= 2:
        print("Error: ID parameter is required", file=sys.stderr)
        print("Error: Check parameter -python run.py <id> <mode>", file=sys.stderr)
        sys.exit(1)  # 1은 에러 코드를 나타냄 (0은 정상 종료)
        
    # data 설정
    set_config(sys.argv)
    
    # 모드 구분
    mode_division()  
        
if __name__ == "__main__":
    main()