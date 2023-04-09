from whoosh.qparser import QueryParser

# Open the index
from whoosh.index import open_dir
ix = open_dir("index")

# Parse a user's query and search the index
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("keyword")
    results = searcher.search(query)
    for result in results:
        print(result["title"])

