from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os

# Define schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Create index in a directory called "index"
if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)

# Open the HTML file and index each news article
writer = ix.writer()
with open("output.html", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("<h1>"):
            title = line[4:-5]
            content = ""
        elif line.startswith("</article>"):
            writer.add_document(title=title, content=content)
        elif line.startswith("<p>"):
            content += line[3:-4] + " "

# Commit changes to the index
writer.commit()

