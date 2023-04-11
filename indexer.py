import os

from whoosh.index import create_in
from whoosh.fields import *

def index():
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

    if not os.path.exists("index"):
        os.mkdir("index")
    ix = create_in("index", schema)

    writer = ix.writer()

    with open("crawler\output.html", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            line = line.lower()
            
            if line.startswith("<h1>"):
                title = line[4:-5]
                content = ""
            elif line.startswith("<article>"):
                content = line[9:-10]
                writer.add_document(title=title, content=content)

    writer.commit()

if __name__ == '__main__':
    index()