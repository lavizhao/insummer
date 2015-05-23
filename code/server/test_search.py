#!/usr/bin/python3

from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, TEXT,STORED
from pprint import pprint

import whoosh.index as index

if __name__ == '__main__':
    index_dir = "/home/lavi/project/insummer/index"
    ix = index.open_dir(index_dir)

    searcher = ix.searcher()
    qp = QueryParser("title", ix.schema)
    q = qp.parse("how can i travel in china ")
    results = searcher.search(q,limit=2222)
    print(len(results))
    for a in results:
        title = a["title"]
        print(title)

    
