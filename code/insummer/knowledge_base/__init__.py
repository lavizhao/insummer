'''
这个模块的作用主要是封装KB的一些功能,变相做接口了
'''

import pymongo
from ..util import NLP,mem_cache
from ..read_conf import config
import sys
import pickle
import time

import multiprocessing as mp

from math import log

SMALL = 1e-6

nlp = NLP()

#读入词表indx
entity_list_file = open(config("../../conf/cn_data.conf")["entity_name"],'rb')
entity_indx = pickle.load(entity_list_file)


class InsunnetFinder:
    def __init__(self):
        self.__usr = 'root'
        self.__pwd = ''
        conn = pymongo.Connection('localhost',27017)
        self.__db = conn.insunnet
        self.tbl = self.__db.assertion
        self.lookup_mc = mem_cache("lookup")

    def lookup(self,entity):

        entity = cp_tool.concept_name(entity)

        result1 = list(self.tbl.find({'start':entity}))
        result2 = list(self.tbl.find({'end':entity}))
        
        result1.extend(result2)

        return result1

    def lookup_weight(self,ent1,ent2):

        ent1 = cp_tool.concept_name(ent1)
        ent2 = cp_tool.concept_name(ent2)

        result1 = list(self.tbl.find({'start':ent1,'end':ent2}))
        result2 = list(self.tbl.find({'start':ent2,'end':ent1}))
        
        result = 0

        if len(result1)==0 and len(result2)==0:
            return 0
        elif len(result1) != 0:
            res = float(result1[0]['weight'])
            return res
        else:
            res1 = float(result2[0]['weight'])
            return res1

#定义与概念相关的常用函数集
#这里要考虑两种情况conceptnet默认的是带/c 的, 而我自己写的不带
class concept_tool(object):
    def __init__(self):
        self.finder = InsunnetFinder()
        
    def is_english_concept(self,cp):
        cp = str(cp)
        if cp.startswith('/c'):
            return cp.startswith('/c/en/')
        else:
            return True

    def both_english_concept(self,cp1,cp2):
        return self.is_english_concept(cp1) and \
            self.is_english_concept(cp2)

    def entity_equal(self,cp1,cp2):
        cp1 = self.concept_name(cp1)
        cp2 = self.concept_name(cp2)
        if cp1 == cp2:
            return True
        else:
            return False
        
    #给concept加/c/en
    def add_prefix(self,entity):
        cp = self.concept_name(entity)
        cp = '/c/en/'+cp
        return cp

    def concept_name(self,entity):
        #去前缀
        entity = str(entity)
        if entity.startswith('/c/en/'):
            entity = entity[6:]
        elif entity.startswith('/c'):
            #如果是其他语言, 那么返回一个在数据库中没有的
            return 'wojiaozhaoximo'
        else:
            entity = entity

        #去后缀
        suffix = entity.find('/')
        if suffix == -1:
            return entity
        else:
            return entity[:suffix]

    #换了个名字,检测kb中是否有概念
    def kb_has_concept(self,concept):
        cp = self.concept_name(concept)
        return cp in entity_indx

    #某个节点的所有邻居
    def neighbours(self,cp):
        cp = self.concept_name(cp)
        edges = self.finder.lookup(cp)
        result = []
        for edge in edges:
            start,end,rel = edge['start'],edge['end'],edge['rel']

            if not self.entity_equal(start,cp):
                result.append(start)

            if not self.entity_equal(start,cp):
                result.append(end)

        return set(result)
        

    def entity_strength(self,cp1,cp2):
        return self.finder.lookup_weight(cp1,cp2)

    def weight_func(self,ent1,base):
        if self.entity_strength(ent1,base) != 0:
            return (base,1)
        else:
            return (base,0)


cp_tool = concept_tool()

