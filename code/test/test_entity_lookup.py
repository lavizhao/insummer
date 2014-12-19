#!/usr/bin/python3

import json
import sys
sys.path.append("..")
import insummer
import profile


from insummer.knowledge_base.entity_lookup import InsunnetEntityLookup as cel
from insummer.knowledge_base import InsunnetFinder as Finder

import time
clock = time.time

my = cel()

finder = Finder()
begin = clock()
result = my.relate_entity_weight(entity='bike')
end = clock()
print(result)
print(end-begin)


