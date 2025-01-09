import json
import os
from elasticsearch import Elasticsearch

from configData import get_argv, get_source, get_search

ARGV = None
SOURCE = None
SEARCH = None

def connect_elasticsearch():
    global SEARCH
    
    SEARCH = get_search()
    
    url = SEARCH._elasticsearch_url
    
    print(f"Elasticsearch Connection URL : {url}")
    
    return Elasticsearch(url)

# json 파일을 elasticsearch에 색인
def to_elasticsearch():
    global ARGV, SOURCE, SEARCH
    
    ARGV = get_argv()
    SOURCE = get_source()
    SEARCH = get_search()

    # Elasticsearch 연결 설정
    es = connect_elasticsearch()

    # json 폴더 경로 설정
    json_dir = os.path.join('json', str(SOURCE._id))
    
    try:
        # 해당 디렉토리의 모든 json 파일 읽기
        for filename in os.listdir(json_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(json_dir, filename)
                
                print(file_path)
                
                # json 파일 읽기
                with open(file_path, 'r', encoding='utf-8') as file:
                    data_list = json.load(file)
                
                # 리스트의 각 항목을 개별적으로 색인
                for item in data_list:
                    try:
                        es.index(
                            index=SOURCE._index,
                            body=item,
                            id=item['url']
                        )
                        
                    except Exception as e:
                        print(f"Error to_elasticsearch Index : {SOURCE._index} - {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return False


# 인덱스 생성
def create_index():
    global ARGV, SOURCE, SEARCH
    
    ARGV = get_argv()
    SOURCE = get_source()
    SEARCH = get_search()
    
    es = Elasticsearch(SEARCH._elasticsearch_url)
    
    es.indices.create(index=f'{SOURCE._index}')
    
    print(f"Index {SOURCE._index} Created")