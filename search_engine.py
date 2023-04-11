from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from unidecode import unidecode

def search(keyword):
    ix = open_dir("index")
    
    final_results = []
    
    with ix.searcher() as searcher:
        keyword = keyword.lower()
        keyword = unidecode(keyword)

        query = QueryParser("data", ix.schema).parse(keyword)
        results = searcher.search(query)
        
        for result in results:
            final_results.append((result["title"], result["content"]))
    
    return final_results