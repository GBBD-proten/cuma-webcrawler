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
        self._id = None
        self._mode = None
        self._json = False
        self._bulk = False
        
        self.load_argv()
        
    def load_argv(self):
        print(f"SELECTED ID: {self.argv[1]}")
        self._id = self.argv[1]
        
        print(f"SELECTED MODE: {self.argv[2]}")
        self._mode = self.argv[2]
        
        if len(self.argv) > 3:
            print(f"SELECTED OPTION: {self.argv[3]}")
            if self.argv[3] == "-json":
                self._json = True
            elif self.argv[3] == "-bulk":
                self._bulk = True

