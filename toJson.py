import json
import os
from datetime import datetime

from configData import get_source

def save_data_to_json(data):
    source = get_source()
    
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
        
