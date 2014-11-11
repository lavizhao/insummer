#!/usr/bin/python3

'''
主要为了测试conceptNet的spreading activities怎么用的
'''

from conceptnet5 import assoc_query
from conceptnet5 import query
from conceptnet5.query import AssertionFinder as Finder

finder = Finder()

dir1 = '/home/lavi/.conceptnet5/assoc/assoc-space-5.3'

my_sa = assoc_query.AssocSpaceWrapper(dir1,finder)

my_sa.load()

#terms = [('/c/en/create',1),('/c/en/website',1)]
#terms = [('/c/en/computer',1),('/c/en/startup',1.5)]
#terms = [('/c/en/facebook',1),('/c/en/website',0.5),('/c/en/work',0.5)]
#terms = [('/c/en/computer',1),('/c/en/open',0.5),('taylor_swift',0.2)]
terms = [('/c/en/virus',1),('/c/en/protection',1),('/c/en/program',1)]
#terms = [('/c/en/youtube',1)]

g = lambda x : x.startswith('/c/en')

result = my_sa.expand_terms(terms)

for term,weight in result:
    if term.startswith('/c/en'):
        print("%20s%20s"%(term[6:],weight))

result1 = my_sa.associations(terms,limit=100)

for term,weight in result1:
    if term.startswith('/c/en'):
        print("%20s%20s"%(term[6:],weight))




