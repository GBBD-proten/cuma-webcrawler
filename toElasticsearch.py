import json
import os
from elasticsearch import Elasticsearch

from configData import get_argv, get_source, get_search



class toElasticsearch:
    ARGV = None
    SOURCE = None
    SEARCH = None
    
    def __init__(self):
        self.ARGV = get_argv()      
        self.SOURCE = get_source()
        self.SEARCH = get_search()
        
    def connect_elasticsearch(self):
        url = self.SEARCH._elasticsearch_url
        
        print(f"[INFO] Elasticsearch Connection URL : {url}")
        
        return Elasticsearch(url)

    # json 파일을 elasticsearch에 색인
    def to_elasticsearch(self):
        
        # Elasticsearch 연결 설정
        es = self.connect_elasticsearch()

        # json 폴더 경로 설정
        json_dir = os.path.join('json', str(self.SOURCE._id))
        
        try:
            index_data_count = 0
            index_success_count = 0
            
            # 해당 디렉토리의 모든 json 파일 읽기
            for filename in os.listdir(json_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(json_dir, filename)
                    
                    # json 파일 읽기
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data_list = json.load(file)
                    
                    index_data_count += len(data_list)
                    
                    # 리스트의 각 항목을 개별적으로 색인
                    for item in data_list:
                        try:
                            es.index(
                                index=self.SOURCE._index,
                                body=item,
                                id=item['url']
                            )
                            
                            index_success_count += 1
                            
                        except Exception as e:
                            print(f"[ERROR] to_elasticsearch Index : {self.SOURCE._index} - {str(e)}")
            
                # 파일 삭제
                os.remove(file_path)
            
            print(f"[INFO] Index {self.SOURCE._index} Data Count : {index_data_count}")
            print(f"[INFO] Index {self.SOURCE._index} Success Count : {index_success_count}")
            return True
            
        except Exception as e:
            print(f"[ERROR] to_elasticsearch : {str(e)}")
            return False


    # 인덱스 생성
    def create_index(self):
        
        es = self.connect_elasticsearch()
        
        es.indices.create(index=f'{self.SOURCE._index}')
        
        print(f"[INFO] Index {self.SOURCE._index} Created")