import json
import os
from datetime import datetime

from configData import getSource

def saveJson(data):
    try:
        source = getSource()
        
        # 폴더 경로 생성
        folder_path = os.path.join('json', str(source._id))
        
        # 폴더가 없으면 생성
        os.makedirs(folder_path, exist_ok=True)
        
        # 현재 시간을 파일명으로 사용
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(folder_path, f'{current_time}.json')
        
        # JSON 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
                
            print(f"Data saved to : {file_path}")
            
            return True
                
    except Exception as e:
        print(f"[ERROR] Failed to save JSON: {str(e)}")
        return False
        
def getIndexName(id):
    try:
        source_file_path = os.path.join('config','source', f'{id}.json')
                
        # source 설정 파일이 존재하는지 확인
        if not os.path.exists(source_file_path):
            raise FileNotFoundError(f"[ERROR] Source file not found: {source_file_path}")
        
        # source JSON 설정 파일 읽기
        with open(source_file_path, 'r', encoding='utf-8') as file:
            source_settings = json.load(file)
            
        # index 값 가져오기
        index_name = source_settings.get('index')
        if not index_name:
            raise ValueError("[ERROR] Index name not found in source file")
        
        return index_name
    except Exception as e:
        print(f"[ERROR] Failed to get index name: {str(e)}")
        return None