'''
这个模块的作用主要是封装KB的一些功能,变相做接口了
'''

import pymongo
from ..util import NLP
from ..read_conf import config
from conceptnet5.query import lookup
from conceptnet5.query import field_match
import sys
import pickle

SMALL = 1e-6

nlp = NLP()

#读入词表indx
entity_list_file = open(config("../../conf/cn_data.conf")["entity_name"],'rb')
entity_indx = pickle.load(entity_list_file)
        
        
#定义与概念相关的常用函数集
#这里要考虑两种情况conceptnet默认的是带/c 的, 而我自己写的不带
class concept_tool(object):
    def __init__(self):
        pass

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

def init_assoc_space():
    assoc_space_dir = '/home/lavi/.conceptnet5/assoc/assoc-space-5.3'
    
    from conceptnet5.query import AssertionFinder as Finder
    finder = Finder()

    sa = NaiveAccocSpaceWrapper(assoc_space_dir,finder)

    return sa
    

cp_tool = concept_tool()

class InsunnetFinder:
    def __init__(self):
        self.__usr = 'root'
        self.__pwd = ''
        conn = pymongo.Connection('localhost',27017)
        self.__db = conn.insunnet
        self.tbl = self.__db.assertion

    def lookup(self,entity):
        entity = cp_tool.concept_name(entity)
        
        result1 = list(self.tbl.find({'start':entity}))
        result2 = list(self.tbl.find({'end':entity}))
        
        result1.extend(result2)

        return result1

        
