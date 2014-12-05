#!/usr/bin/python3

import json
import sys
sys.path.append("..")
import insummer
import profile


from insummer.knowledge_base.entity_lookup import ConceptnetEntityLookup
from insummer.knowledge_base import concept_tool
from insummer.query_expansion.entity_expansioner import OnlySynExpansioner,SynRelateExpansioner
from insummer.common_type import Question
from insummer.query_expansion.entity_finder import example_entity_finder,NgramEntityFinder

import data
questions = data.get_data()

cn = concept_tool()
finder = NgramEntityFinder

#title = "How do Motorcycles pollute?"
#title = "what's wrong with my bike?"


if __name__ == '__main__':

    #for i in range(len(questions)):
    for i in range(1):
        print(i)
        q = questions[i]
        #exp = OnlySynExpansioner(q,finder,max_level=2,display=True)
        exp = SynRelateExpansioner(q,finder,max_level=1,display=True)
        exp.run()
        #ose.construct_sentence_entity()
        print(100*"-")
    #ose.construct_sentence_entity()
    #ose.print_sentence_entity()

 
