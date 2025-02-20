class ArgvData:
    _instance = None
    
    @classmethod
    def getInstance(cls, argv=None):
        if cls._instance is None:
            cls._instance = cls(argv)
        return cls._instance
    
    def __init__(self, argv=None):
        print(f"argv: {argv}")
        if argv is None:
            return
        
        self.argv = argv
        self._id = None
        self._mode = None
        self._json = False
        self._bulk = False
        self._debug = False
        self._test = False
        self._test_count = 0

        self.loadArgv()
        
    def loadArgv(self):
        print(f"SELECTED ID: {self.argv[1]}")
        self._id = self.argv[1]
        
        print(f"SELECTED MODE: {self.argv[2]}")
        self._mode = self.argv[2]
        
        if len(self.argv) > 3:
            print(f"SELECTED OPTION: {self.argv[3:]}")
            if '-json' in self.argv:
                self._json = True
            if '-bulk' in self.argv:
                self._bulk = True
            if '-json' not in self.argv and '-bulk' not in self.argv:
                self._json = True
                self._bulk = True
            if '-debug' in self.argv:
                self._debug = True
            
            if '-test' in self.argv:
                self._test = True
                test_index = self.argv.index('-test')
                
                # -test 다음 인덱스에 숫자가 있는지 확인
                if test_index + 1 < len(self.argv):
                    try:
                        self._test_count = int(self.argv[test_index + 1])
                    except ValueError:
                        # 숫자가 아닌 경우 무시
                        pass
                    
                    print(f"TEST COUNT: {self._test_count}")

