import sys

from argv import ArgvData
from crawler import crawl_site_division
from toJson import save_data_to_json

def main():
    if len(sys.argv) <= 1:
        print("Error: ID parameter is required", file=sys.stderr)
        print("Error: Check parameter -python run.py <id> <option>", file=sys.stderr)
        sys.exit(1)  # 1은 에러 코드를 나타냄 (0은 정상 종료)
        
    argv_data = ArgvData.get_instance(sys.argv)

    crawl_data = crawl_site_division()
    
    save_data_to_json(crawl_data, argv_data._id)
        
if __name__ == "__main__":
    main()