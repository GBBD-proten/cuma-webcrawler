from config import ArgvData, SourceData, SearchData

ARGV = None
SOURCE = None
SEARCH = None

def set_config(argv):
    global ARGV, SOURCE, SEARCH
    ARGV = ArgvData.get_instance(argv)
    SOURCE = SourceData.get_instance(argv[1])
    SEARCH = SearchData.get_instance()
    
    
def get_argv():
    return ARGV

def get_source():
    return SOURCE

def get_search():
    return SEARCH