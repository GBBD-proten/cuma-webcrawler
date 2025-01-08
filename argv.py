class ArgvData:
    _instance = None
    
    @classmethod
    def get_instance(cls, argv=None):
        if cls._instance is None:
            cls._instance = cls(argv)
        return cls._instance
    
    def __init__(self, argv=None):
        if argv is None:
            return
        
        self.argv = argv
        self._json = False
        self._bulk = False
        
        self._load_data()
        
    def _load_data(self):
        print(f"SELECTED ID: {self.argv[1]}")
        self._id = self.argv[1]
        
        if len(self.argv) > 2:
            print(f"SELECTED OPTION: {self.argv[2]}")
            if self.argv[2] == "-json":
                self._json = True
            elif self.argv[2] == "-bulk":
                self._bulk = True

