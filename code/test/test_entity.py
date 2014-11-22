#!/usr/bin/python3

import json
import sys
sys.path.append("..")
import insummer


from insummer.knowledge_base.entity_lookup import ConceptnetEntityLookup
from insummer.knowledge_base import concept_tool

cn = concept_tool()

if __name__ == '__main__':
    print("hello")
    cel = ConceptnetEntityLookup()
    entity = 'pollute'

    result = cel.synonym_entity(entity)

    for i in result:
        print(cn.concept_name(i))

