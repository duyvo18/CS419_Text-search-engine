from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from unidecode import unidecode

def search(keyword):
    ix = open_dir("index")
    
    final_results = []
    
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(keyword)
        results = searcher.search(query)
        
        for result in results:
            final_results.append((result["title"], result["content"]))
        
        query_unicode = QueryParser("content", ix.schema).parse(unidecode(keyword))
        results_unicode = searcher.search(query_unicode)
        
        for result in results_unicode:
            final_results.append((result["title"], result["content"]))
    
    return final_results