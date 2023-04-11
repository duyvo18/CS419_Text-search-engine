# Text-based Search Engine

## Setup

1. Install the required packages with `python -m pip install -r requirement.txt`

## To run the Search Engine

1. Run the search engine with `streamlit run main.py`

## To renew the index

1. Run `indexer.py` with `python indexer.py`

## Notes

* `indexer.py` defines the indexing process
* `search_engine.py` defines the searching function
* `main.py` defines the streamlit interface and call `search_engine.search(keyword)` to query
* `crawler/` defines the Scrapy crawler
* The crawled data is in `crawler/output.html`
