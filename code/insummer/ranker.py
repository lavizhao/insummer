'''
对图进行rank的类
'''

import sys
from abc import ABCMeta, abstractmethod
from .knowledge_base import concept_tool
from .evaluation import bias_overlap_ratio,bias_overlap_quantity

import networkx as nx
import itertools
from operator import itemgetter
import matplotlib.pyplot as plt

cn = concept_tool()

def get_weight1(ent1,ent2):
    weight = cn.entity_strength(ent1,ent2)
    if ent1 == ent2 :
        return 1
    else:
        return weight

def get_weight2(ent1,ent2):
    weight = cn.entity_strength(ent1,ent2)
    if ent1 == ent2 or weight != 0:
        return 1
    else:
        return 0

#给定一群实体, 最后得出这些实体的重要性
class abstract_ranker(metaclass=ABCMeta):
    def __init__(self,entity):
        self.__entity = entity
        self.__graph = None
        
    def get_entity(self):
        return self.__entity

    def get_graph(self):
        return self.__graph

    def set_graph(self,gr):
        self.__graph = gr
        return self.__graph
        
    def build_graph(self):
        entity =  self.get_entity()
        
        gr = nx.Graph()
        gr.add_nodes_from(entity)
        node_pairs = list(itertools.combinations(entity,2))

        for ent1,ent2 in node_pairs:
            weight = get_weight2(ent1,ent2)
            if weight > 0:
                gr.add_edge(ent1,ent2,weight=weight)

        return self.set_graph(gr)

    #返回类型, 可以为set和dict两种, 一种带weight一种不带
    @abstractmethod
    def rank(self,return_type="set"):
        pass


class Hitsranker(abstract_ranker):
    def __init__(self,entity):
        abstract_ranker.__init__(self,entity)

    def rank(self,return_type='set'):
        #排除一些异常情况    
        graph = self.get_graph()
        if graph==None:
            graph = self.build_graph()


        h,a = nx.hits(graph,max_iter = 300)

        imp = a

        result = sorted(imp.items(), key=lambda d: d[1],reverse=True)

        if return_type == 'set':
            result = [x for (x,y) in result]
            return result
        else:
            return result

    
        
class Pageranker(abstract_ranker):
    def __init__(self,entity):
        abstract_ranker.__init__(self,entity)

    #==================重载方法=======================
    def build_graph(self):
        entity =  self.get_entity()
        
        gr = nx.Graph()
        gr.add_nodes_from(entity)
        node_pairs = list(itertools.combinations(entity,2))

        for ent1,ent2 in node_pairs:
            weight = get_weight2(ent1,ent2)
            if weight > 0:
                gr.add_edge(ent1,ent2,weight=weight)


        #去掉0初度的点, 防止pagerank报错
        W = nx.DiGraph(gr)    
        degree = W.out_degree(weight='weight')
        for(u,v,d) in W.edges(data=True):
            if degree[u] == 0:
                try:
                    gr.remove_node(u)
                except:
                    pass

                
        return self.set_graph(gr)

    def rank(self,return_type='set'):
        #排除一些异常情况    
        graph = self.get_graph()
        if graph==None:
            graph = self.build_graph()

        entity = self.get_entity()
        person = {}            
        for ent in graph.nodes():
            if ent in entity:
                person[ent] = 1
            else:
                person[ent] = 0.5

        pr = nx.pagerank_numpy(graph,weight='weight',alpha=0.8,personalization=person)
        result = sorted(pr.items(), key=lambda d: d[1],reverse=True)

        if return_type == 'set':
            result = [x for (x,y) in result]
            return result
        else:
            return result



#用连通度做排序
#===============================> 这个排序方法其实做的不好            
class CCRanker(abstract_ranker):
    def __init__(self,entity):
        abstract_ranker.__init__(self,entity)
        
    def rank(self,return_type='set'):
        entity = self.get_entity()
        
        graph = self.get_graph()
        if graph==None:
            graph = self.build_graph()

        sub_graphs = nx.connected_component_subgraphs(graph)

        result = set()
        
        for sub in sub_graphs:
            nodes = set(sub.nodes())
            if len(nodes.intersection(entity)) >= 10:
                result = result.union(nodes)

        if return_type == 'set':
            return result
        else:
            result = {ite:1 for ite in result}
            return result


class KCoreRanker(abstract_ranker):
    def __init__(self,entity):
        abstract_ranker.__init__(self,entity)

    def rank(self,return_type='set'):
        entity = self.get_entity()
        
        graph = self.get_graph()
        if graph==None:
            graph = self.build_graph()

        sub_graphs = nx.connected_component_subgraphs(graph)

        result = set()
        
        result = set(nx.k_core(graph,k=3).nodes())
        
        if return_type == 'set':
            return result
        else:
            result = {ite:1 for ite in result}
            return result

