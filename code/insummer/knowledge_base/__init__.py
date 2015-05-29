'''
这个模块的作用主要是封装KB的一些功能,变相做接口了
'''

import pymongo
from ..util import NLP,mem_cache
from ..read_conf import config
from conceptnet5.query import lookup
from conceptnet5.query import field_match
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

    ###这个函数已经不用了
    #这个函数的作用是检测概念是否在conceptNet中,如果在则返回true, 如果不在返回false
    def __conceptnet_has_concept_sqlite(self,concept):
        ans1 = lookup('/c/en/'+concept)
        indx = 0
        for item in ans1:
            indx += 1
            if indx > 0:
                break

        if indx > 0:
            return True

        return False

    #这个是改进版本的查找实体函数, 主要是把索引单独拿出来存到内存了, 效率提高了10倍
    def conceptnet_has_concept(self,concept):
        return concept in entity_indx

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
        
    #计算实体相似度
    def concept_similarity(self,cp1,cp2):
        cp1,cp2 = self.concept_name(cp1),self.concept_name(cp2)

        #如果有一个不在知识库中,则返回-1
        if not self.kb_has_concept(cp1) or not self.kb_has_concept(cp2):
            return -1

        #返回节点的邻居
        n1 = self.neighbours(cp1)
        n2 = self.neighbours(cp2)

        intersection = n1.intersection(n2)
        union = n1.union(n2)

        if len(n1) == 0 or len(n2) == 0:
            return 0

        print(len(n1),len(n2),len(intersection),len(union))
            
        #return len(n1.intersection(n2)) / min(len(n1),len(n2))
        return 1 - (log(max(len(n1),len(n2))) - log(len(intersection)) ) / \
            (log(len(union)) - log(min(len(n1),len(n2)))  ) 

    def entity_strength(self,cp1,cp2):
        return self.finder.lookup_weight(cp1,cp2)

    def weight_func(self,ent1,base):
        if self.entity_strength(ent1,base) != 0:
            return (base,1)
        else:
            return (base,0)

    def multi_lookup(self,base_entity,entity):
        pool = mp.Pool(processes=2)
        print(base_entity)
        results = [pool.apply_async(self.weight_func, args=(entity,base_entity[i],)) for i in range(len(base_entity))]
        output = [p.get() for p in results]
        return output

        
    def cube(self,x):
        return x
#试验品
class NaiveAccocSpaceWrapper(object):
    def __init__(self,path,finder):
        self.path = path
        self.finder = finder
        self.assoc = None

    def load(self):
        if self.assoc is not None:
            return

        try:
            from assoc_space import AssocSpace
            self.assoc = AssocSpace.load_dir(self.path)

        except:
            print("error in import assoc space")
            sys.exit(1)

    @staticmethod
    def passes_filter(label, filter):
        if filter == None:
            return True
        else:
            return field_match(label, filter)

    def expand_terms(self, terms, limit_per_term=10):
        """
        Given a list of weighted terms, add terms that are one step away in
        ConceptNet at a lower weight.

        This helps increase the recall power of the AssocSpace, because it
        means you can find terms that are too infrequent to have their own
        vector by looking up their neighbors. This forms a reasonable
        approximation of the vector an infrequent term would have anyway.
        """
        self.load()
        expanded = terms[:]
        for term, weight in terms:
            for edge in self.finder.lookup(term, limit=limit_per_term):
                if field_match(edge['start'], term):
                    neighbor = edge['end']
                elif field_match(edge['end'], term):
                    neighbor = edge['start']
                else:
                    continue
                neighbor_weight = weight * edge['weight'] * 0.1
                if edge['rel'].startswith('/r/Not'):
                    neighbor_weight *= -1
                expanded.append((neighbor, neighbor_weight))

        total_weight = sum(abs(weight) for (term, weight) in expanded)
        if total_weight == 0:
            return []
        return [(term, weight / total_weight) for (term, weight) in expanded]

    def norm_terms(self,terms):
        total_weight = sum(abs(weight) for (term, weight) in terms)
        if total_weight == 0:
            return []
        return [(term, weight / total_weight) for (term, weight) in terms]

    def associations(self, terms, filter=None, limit=20):
        self.load()
        vec = self.assoc.vector_from_terms(self.expand_terms(terms))
        #vec = self.assoc.vector_from_terms(self.norm_terms(terms))
        similar = self.assoc.terms_similar_to_vector(vec)
        similar = [
            item for item in similar if item[1] > SMALL
            and self.passes_filter(item[0], filter)
        ][:limit]
        return similar

    def sim(self,t1,t2):
        self.load()    
        return self.assoc.assoc_between_two_terms(t1,t2)


        
'''        
def init_assoc_space():
    assoc_space_dir = '/home/lavi/.conceptnet5/assoc/assoc-space-5.3'
    
    from conceptnet5.query import AssertionFinder as Finder
    finder = Finder()

    sa = NaiveAccocSpaceWrapper(assoc_space_dir,finder)

    return sa
'''    

cp_tool = concept_tool()

