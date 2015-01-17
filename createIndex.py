import os.path
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.analysis import StandardAnalyzer,StemmingAnalyzer

def createIndex():
    """Create Whoosh index directory."""

    ana = StemmingAnalyzer(cachesize=-1)
    
    schema = Schema(content=TEXT(stored=True,analyzer=ana),tags=TEXT(stored=True))
    
    if not os.path.exists("index"):
        os.mkdir("index")
    
    index = create_in("index", schema)
    
if __name__ == "__main__":
    createIndex()