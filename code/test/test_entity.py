#!/usr/bin/python3

import json
import sys
sys.path.append("..")
import insummer


from insummer.knowledge_base.entity_lookup import ConceptnetEntityLookup
from insummer.knowledge_base import concept_tool
from insummer.query_expansion.entity_expansioner import OnlySynExpansioner
from insummer.common_type import Question
from insummer.query_expansion.entity_finder import example_entity_finder,NgramEntityFinder

cn = concept_tool()
finder = NgramEntityFinder

title = "How do Motorcycles pollute?"
#title = "what's wrong with my bike?"

fuck = Question(title,"","",[])

if __name__ == '__main__':
    print("hello")
    entity = 'pollute'

    ose = OnlySynExpansioner(fuck,finder)
    result = ose.expand()

    for i in result:
        print(i)

