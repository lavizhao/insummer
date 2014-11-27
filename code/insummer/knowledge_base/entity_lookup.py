'''
这个文件的作用是定义一个实体查找的借口, 这个借口的作用是可以进行替换
为什么要这么设计: 因为可能用conceptnet默认的会比较困难, 所以需要做一些查询时间上的优化
'''

import pymongo

from conceptnet5.query import AssertionFinder as Finder

from .import InsunnetFinder

from . import concept_tool
cn_tool = concept_tool()

from .relation import relation_tool
rel_tool = relation_tool()

from abc import ABCMeta, abstractmethod


class abstract_entity_lookup(metaclass=ABCMeta):
    def __init__(self):
        pass

    #抽象方法, 查找同一实体,这里一定要注意, 这里是在单层寻找同一实体
    #比如 A和B同义, B和C同义, 如果查找A的同义实体的时候, 要B, 但是C是第二层的不要
    #如果是在有必要的话, 可能考虑后期重构, 但是现在我觉得这样实现好一些
    #穿进来的是一个entity, 没有加/c/en 的
    @abstractmethod
    def synonym_entity(self,entity):
        pass

    #通过reltype来抽取合格的属性, reltype是函数, relation里面定义
    #synonym_entity等方法可以调用该方法
    #其他附加条件, 接口留了, 到时候随意
    @abstractmethod
    def lookup_entity_with_reltype():
        pass

#这个定义通用的concept限制条件, 一般都会用这个, 
def common_limit(cp1,cp2,rel,cp):
    if cn_tool.both_english_concept(cp1,cp2):
        return True
    else:
        return False
    
#这个是利用conceptnet进行查找的类, 这个速度肯定不会快
class ConceptnetEntityLookup(abstract_entity_lookup):

    def __init__(self):
        abstract_entity_lookup.__init__(self)
        self.cn_finder = Finder()


    def lookup_entity_with_reltype(self,entity,reltype,other_limit=None):

        #先加个前缀
        entity = cn_tool.add_prefix(entity)

        result = []
        
        #对于能查到的每个结构关系
        for edge in self.cn_finder.lookup(entity):
            #获得三元组
            start,end,rel = edge['start'],edge['end'],edge['rel']

            #如果实体==end,则neighbour=start, 反之=end
            #这个实体相等是可以自动去前后缀的
            neighbour = start if cn_tool.entity_equal(end,entity) else end

            #如果满足某个条件
            if reltype(rel) :
                if other_limit != None :
                    if other_limit(start,end,rel,entity):
                        result.append(neighbour)
                        #print("start %30s || rel %20s ||end %30s"%(cn_tool.concept_name(start),rel,cn_tool.concept_name(end)))    
                else:
                    result.append(neighbour)

        #重新去一遍前后缀
        result = self.remove_prefix_suffix(result)                    
        return result

    def remove_prefix_suffix(self,entity_list):
        result = set()
        for i in entity_list:
            result.add(cn_tool.concept_name(i))

        return result
        
    def synonym_entity(self,entity):
        result = self.lookup_entity_with_reltype(entity,rel_tool.synonym_type,common_limit)

        return result

    #关联关系
    def relate_entity(self,entity):
        result = self.lookup_entity_with_reltype(entity,rel_tool.relate_type,common_limit)
        return result



def insun_limit(cp1,cp2,rel,cp):
    return True
        
#这个是利用conceptnet进行查找的类, 这个速度肯定不会快
class InsunnetEntityLookup(abstract_entity_lookup):

    def __init__(self):
        abstract_entity_lookup.__init__(self)
        self.cn_finder = InsunnetFinder()
        

    def lookup_entity_with_reltype(self,entity,reltype,other_limit=None):

        #先加个前缀
        entity = str(entity)
        entity = cn_tool.add_prefix(entity)

        result = []

        edges = self.cn_finder.lookup(entity)

        #对于能查到的每个结构关系
        for edge in edges:
            #获得三元组
            start,end,rel = edge['start'],edge['end'],edge['rel']

            #如果实体==end,则neighbour=start, 反之=end
            #这个实体相等是可以自动去前后缀的
            neighbour = start if cn_tool.entity_equal(end,entity) else end

            #如果满足某个条件
            if reltype(rel) :
                if other_limit != None :
                    if other_limit(start,end,rel,entity):
                        result.append(neighbour)
                        #print("start %30s || rel %20s ||end %30s"%(cn_tool.concept_name(start),rel,cn_tool.concept_name(end)))    
                else:
                    result.append(neighbour)

        #重新去一遍前后缀
        #result = self.remove_prefix_suffix(result)                    
        return result

    def remove_prefix_suffix(self,entity_list):
        result = set()
        for i in entity_list:
            result.add(cn_tool.concept_name(i))

        return result
        
    def synonym_entity(self,entity):
        result = self.lookup_entity_with_reltype(entity,rel_tool.synonym_type,insun_limit)

        return result

    #关联关系
    def relate_entity(self,entity):
        result = self.lookup_entity_with_reltype(entity,rel_tool.relate_type,insun_limit)
        return result
        
