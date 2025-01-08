import json
import os

class SourceData:
    _instance = None
    
    @classmethod
    def get_instance(cls, id=None):
        if cls._instance is None:
            cls._instance = cls(id)
        return cls._instance
    
    def __init__(self, id):
        if id is None:
            return
            
        self._id = id
        self._index = None
        self._site = None
        self._site_name = None
        self._site_type = None
        self._category = None
        self._category_name = None
        self._contents = None
        self._url = None
        self._parameter = None
        self._max_parameter = None
        self._min_parameter = None
        self._info = None
        
        self._load_data()
    
    def _load_data(self):
        source_dir = 'source'
        json_file = f"{self._id}.json"
        file_path = os.path.join(source_dir, json_file)
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._index = data['index']
                self._site = data['site']
                self._site_name = data['site_name']
                self._site_type = data['site_type']
                self._category = data['category']
                self._category_name = data['category_name']
                self._contents = data['contents']
                self._url = data['link']['url']
                self._parameter = data['link']['parameter']
                self._max_parameter = data['link']['max_parameter']
                self._min_parameter = data['link']['min_parameter']
                self._info = data['info']
            else:
                print({"error": f"ID {self._id} is not exist json file."})
        except Exception as e:
            print({"error": f"json file read error: {str(e)}"})
