from config import ArgvData, SourceData, SearchData

ARGV = None
SOURCE = None
SEARCH = None

def setConfig(argv):
    global ARGV, SOURCE, SEARCH
    ARGV = ArgvData.getInstance(argv)
    SOURCE = SourceData.getInstance(argv[1])
    SEARCH = SearchData.getInstance()
    
    
def getArgv():
    return ARGV

def getSource():
    return SOURCE

def getSearch():
    return SEARCH