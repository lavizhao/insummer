#!/usr/bin/python3

entity = {'male', 'battery', 'barrier', 'automobile', 'admittance', 'admission', 'way', 'dobbin', 'entrée', 'access', 'nag', 'car', 'jade', 'ink', 'bung', 'vehicle', 'carload', 'railcar', 'auto_insurance', 'carriage', 'motor', 'gondola', 'electricity', 'car_battery', 'wagonload', 'entry', 'motorcar', 'auto', 'male-to-female', 'electroconvulsive_therapy', 'wagon', 'tramcar', 'plug', 'ect', 'military_battery', 'stopper', 'electric_power', 'electrical_power', 'username', 'accumulator', 'basket', 'hack'}

base = {'car_battery', 'battery', 'plug', 'ect', 'car', 'electricity', 'access'}

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

import networkx as nx
import itertools
from operator import itemgetter
import matplotlib.pyplot as plt

#title = "How do Motorcycles pollute?"
#title = "what's wrong with my bike?"

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


from collections import defaultdict
import networkx as nx
import numpy
from scipy.cluster import hierarchy,vq
from scipy.spatial import distance
import matplotlib.pyplot as plt

def create_hc(G, t=1.2):
    """
    从距离矩阵中创造一个图G的分层聚类
    马克西姆注：对带有标签的图进行聚类的前处理和后处理，并返回聚类的结果
    参数化门槛值之后，其取值范围应该通过对每个数据进行尝试的基础上确定
    """
    """在对德鲁•康威（Drew Conway）编写的代码进行优化的基础上而来"""
    ## 创造最短路径距离矩阵，但是保留节点标签
    labels=list(G.nodes())
    indx = {}
    
    for ind in range(len(labels)):
        word = labels[ind]
        indx[word] = ind
        
    path_length=nx.all_pairs_shortest_path_length(G)

    distances=numpy.zeros((len(G),len(G)))
    for i in range(len(labels)):
        for j in range(len(labels)):
            distances[i][j] = 10000

    for u,p in path_length.items():
        uind = indx[u]
        for v,d in p.items():
            vind = indx[v]
            #u和v 都是词
            distances[uind][vind]=d

    # 创造分层聚类
    Y=distance.squareform(distances)
    #Z=hierarchy.single(Y)
    Z=hierarchy.average(Y) 
    print("caonima",Z.shape)
    # 这种划分的选择是任意的，仅仅为了说明 的目的
    membership=list(hierarchy.fcluster(Z,t=t))
    
    partition=defaultdict(list)
    for n,p in zip(list(range(len(G))),membership):
        partition[p].append(labels[n])
    return list(partition.values())
        
        
if __name__ == '__main__':

    print("测试是不是所有实体都在知识库中")
    for ent in entity:
        if not cn.kb_has_concept(ent):
            print("error")

    print("下面建立网络")

    gr = nx.Graph()#建立一个无向图
    gr.add_nodes_from(entity)

    nodePairs = list(itertools.combinations(entity,2))

    person = {}
    for ent in entity:
        if ent in base:
            person[ent] = 1
        else:
            person[ent] = 0.5

    for pair in nodePairs:
        ent1,ent2 = pair[0],pair[1]
        weight = get_weight2(ent1,ent2)
        if weight > 0:
            gr.add_edge(ent1,ent2,weight=weight)

    #nx.draw(gr)
    #plt.show()        

    print("page rank")
    pr = nx.pagerank(gr,weight='weight',alpha=0.85,personalization=person,max_iter=400)
    keyphrases = sorted(pr, key=pr.get, reverse=True)

    for i in keyphrases:
        print(i,pr[i])

    print(keyphrases)

    print("scc")

    #G is the networkx graph 
    sub_graphs = nx.connected_component_subgraphs(gr)

    #n gives the number of sub graphs
    n = len(sub_graphs)

    # you can now loop through all nodes in each sub graph
    for i in range(n):
        print("Subgraph:", i, "consists of ",sub_graphs[i].nodes())
        
    print("cluster")
    result = create_hc(gr)
    for sub in result:
        print(sub)


    print("hits")
    h,a = nx.hits(gr)
    print(sorted(a.items(), key=lambda d: d[1] , reverse=True) )
    
