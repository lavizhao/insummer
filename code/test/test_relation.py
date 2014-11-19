#!/usr/bin/python3

import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config
from insummer.knowledge_base import concept_tool
from insummer.knowledge_base.relation import relation_tool

rel_tool = relation_tool()

if __name__ == '__main__':
    rel = '/r/NotIsA'
    positive = 'pos' if rel_tool.is_pos(rel) else 'neg'
    
    print(rel_tool.rel_name(rel))
    print(positive)

