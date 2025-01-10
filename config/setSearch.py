import json
import os

class SearchData:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self._elasticsearch_url = None
        
        self.load_config()
        
    def load_config(self):
        config_dir = 'config'
        json_file = 'search.json'
        file_path = os.path.join(config_dir, json_file)
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self._elasticsearch_url = data['elastic']['host'] + ':' + data['elastic']['port']
            else:
                print({"error": f"file [{file_path}] is not exist config file."})
        except Exception as e:
            print({"error": f"config file read error: {str(e)}"})