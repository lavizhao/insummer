#!/usr/bin/python3
#coding=utf-8

from datetime import datetime
import itertools
import networkx as nx
import pickle
from abstract_type import abstract_type
import sys
sys.path.append('..')
import insummer
from insummer.common_type import Question,Answer
from insummer.read_conf import config
from insummer.util import NLP
from insummer.query_expansion.entity_finder import NgramEntityFinder

#获得问题的路径信息
question_conf = config('../../conf/question.conf')
filter_path = question_conf['filter_qa']
duc_path = question_conf['duc_question']
filter_abstract = question_conf['filter_abstract']
duc_abstract = question_conf['duc_abstract']

nlp = NLP()

#xx_quesiton里面即问题列表
filter_file = open(filter_path,'rb')
filter_quesiton = pickle.load(filter_file)
#duc_file = open(duc_path,'rb')
#duc_question = pickle.load(duc_file)

#single_question => nbest_content => top_k sents => abstract
def get_abstract(questions,q_path,K):
    "根据问题list获得摘要list"
    abstract_list = []
    for idx,s_question in enumerate(questions):
        print('处理第 %s 个问题'%idx)
        start_time = datetime.now()
        title = s_question.get_title()
        answer_text = s_question.get_nbest_content()
        tmp_abstract = abstract_type(title,answer_text)
        abstract_text = ExtractSentence(answer_text,K)
        tmp_abstract.update_abstract(abstract_text)
        abstract_list.append(tmp_abstract)
        times = datetime.now() - start_time
        print("text_length : %s  used_time : %s \n abstract : %s"%(len(answer_text),times,abstract_text))
    #out_file = open(q_path,'wb')
    #pickle.dump(abstract_list,out_file,True)

#text => sentences => graph => calculate => scores
def ExtractSentence(text,k):
    "根据文本内容获得句子重要性排名"
    print('开始句子重要性排名')
    sent_tokens = nlp.sent_tokenize(text)
    text_graph = graph_construct(sent_tokens)
    cal_gr_page_rank = nx.pagerank(text_graph,weight='weight')
    sents = sorted(cal_gr_page_rank,key = cal_gr_page_rank.get, reverse=True)
    return ' '.join(sents[:k])

def graph_construct(nodes):
    "构建text_rank_graph"
    print('构建text_graph')
    text_graph = nx.Graph()
    text_graph.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes,2))
    for pair in nodePairs:
        first_sent = pair[0]
        sencond_sent = pair[1]
        weights = lDistance(first_sent,sencond_sent)
        text_graph.add_edge(first_sent,sencond_sent,weight=weights)
    print('graph construction end.')
    return text_graph

def lDistance(firstString, secondString):
    "Function to find the Levenshtein distance between two words/sentences"
    if len(firstString) > len(secondString):
        firstString, secondString = secondString, firstString
    distances = range(len(firstString) + 1)
    for index2, char2 in enumerate(secondString):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(firstString):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]   

if __name__ == "__main__":
    get_abstract(filter_quesiton,filter_abstract,4)
