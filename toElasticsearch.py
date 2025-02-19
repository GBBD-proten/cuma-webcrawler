import json
import os
from elasticsearch import Elasticsearch

from configData import getArgv, getSource, getSearch
from toJson import getIndexName



class toElasticsearch:
    ARGV = None
    SOURCE = None
    SEARCH = None
    
    def __init__(self):
        self.ARGV = getArgv()      
        self.SOURCE = getSource()
        self.SEARCH = getSearch()
        
        # 클래스 초기화 시 ES 연결 생성
        self.es = self.connect_elasticsearch()
        
    def connect_elasticsearch(self):
        url = self.SEARCH._elasticsearch_url
        
        return Elasticsearch(url)

    # json 파일을 elasticsearch에 색인
    def toElasticsearch(self):

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
                            self.es.index(
                                index=self.SOURCE._index,
                                body=item,
                                id=item['url']
                            )
                            
                            index_success_count += 1
                            
                        except Exception as e:
                            print(f"[ERROR] to_elasticsearch Index : {self.SOURCE._index} - {str(e)}")
            
                # 파일 삭제
                # os.remove(file_path)
            
            print(f"[INFO] Index {self.SOURCE._index} Data Count : {index_data_count}")
            print(f"[INFO] Index {self.SOURCE._index} Success Count : {index_success_count}")
            
            self.closeElasticsearch()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] to_elasticsearch : {str(e)}")
            return False

    # 인덱스 생성
    def createIndex(self):
        try:
            index_name = getIndexName(self.ARGV._id)
            
            # index 폴더에서 해당 인덱스 설정 파일 찾기
            index_file_path = os.path.join('config','index', f'{index_name}.json')
            
            # index 설정 파일이 존재하는지 확인
            if not os.path.exists(index_file_path):
                raise FileNotFoundError(f"[ERROR] Index file not found: {index_file_path}")
            
            # index JSON 설정 파일 읽기
            with open(index_file_path, 'r', encoding='utf-8') as file:
                index_settings = json.load(file)
            
            # 인덱스 생성
            self.es.indices.create(
                index=self.SOURCE._index,
                body=index_settings
            )
            
            print(f"[INFO] Index {self.SOURCE._index} Created with custom settings")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to create index: {str(e)}")
            return False
        
    def deleteIndex(self):
        try:
            index_name = getIndexName(self.ARGV._id)
            
            self.es.indices.delete(index=index_name)
            
            print(f"[INFO] Index {index_name} Deleted")
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to delete index: {str(e)}")
            return False
        
    # 수집한 URL 중복 체크
    def urlCheck(self, url):
        
        response = self.es.search(index=self.SOURCE._index, body={"query": {"match": {"url": url}}})
        
        return response['hits']['total']['value']
        
    def closeElasticsearch(self):
        self.es.close()
        