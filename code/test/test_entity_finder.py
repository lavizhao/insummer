#!/usr/bin/python3

import sys
sys.path.append("..")
import insummer
from insummer.query_expansion1.entity_finder import example_entity_finder
from insummer.read_conf import config
from insummer.common_type import Question

def test1():
    naive_question = Question("sh",None,None,None)

    my = example_entity_finder(naive_question)

    my.find()
    my.print()
    
if __name__ == '__main__':
    test1()
    

