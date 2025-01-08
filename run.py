import sys
from argv import ArgvData
from crawler import main_crawl

def main():
    if len(sys.argv) <= 1:
        print("Error: ID parameter is required", file=sys.stderr)
        print("Error: Check parameter -python run.py <id> <option>", file=sys.stderr)
        sys.exit(1)  # 1은 에러 코드를 나타냄 (0은 정상 종료)
        
    argv_data = ArgvData.get_instance(sys.argv)
     
            
    main_crawl()
        
if __name__ == "__main__":
    main()