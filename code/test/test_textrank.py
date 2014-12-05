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
        gr.add_edge(ent1,ent2,weight=weight)

    print("page rank")
    pr = nx.pagerank(gr,weight='weight',alpha=0.85,personalization=person,max_iter=400)
    keyphrases = sorted(pr, key=pr.get, reverse=True)

    for i in keyphrases:
        print(i,pr[i])

    print(keyphrases)
