#!/usr/bin/python3
#coding=utf-8

from datetime import datetime
import itertools
import networkx as nx
import pickle
import math
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

#为了ROUGE要将每个topic分开存放到duc/sum_result中
textrank_path = question_conf['textrank_sum']

nlp = NLP()

#xx_quesiton里面即问题列表
filter_file = open(filter_path,'rb')
filter_quesiton = pickle.load(filter_file)
duc_file = open(duc_path,'rb')
duc_question = pickle.load(duc_file)

#single_question => nbest_content => top_k sents => abstract
def get_abstract(questions,q_path,K):
    "根据问题list获得摘要list"
    abstract_list = []
    for idx,s_question in enumerate(questions):
        print('处理第 %s 个问题'%idx)
        start_time = datetime.now()
        
        #获得标题和答案的文本，修改了commontype里面的get_nbest_content函数，返回以空格链接的答案
        title = s_question.get_title()
        answer_text = s_question.get_nbest_content()

        #为每个答案创建一个摘要类，以标题和答案初始化
        tmp_abstract = abstract_type(title,answer_text)

        #对某一答案抽取topK个句子作为摘要，需改成限定词语数量。
        abstract_text = ExtractSentence(answer_text,K)

        #为了ROUGE，存放单个摘要，文件名用topic名D0701A etc.
        filename = s_question.get_author()
        if filename[-1] == '/':
            filename = filename[:-1]
        sum_path = textrank_path + filename
        with open(sum_path,'w') as sum_file:
            sum_file.write(abstract_text)
            print('abstract for %s is wrote..'%filename)
        sum_file.close()

        #保存并添加到摘要list中，准备扔到pickle里
        tmp_abstract.update_abstract(abstract_text)
        abstract_list.append(tmp_abstract)

        times = datetime.now() - start_time
        print("text_length : %s  used_time : %s \n abstract : %s"%(len(answer_text),times,abstract_text))

    #将duc或者filter的所有问题和相应的摘要保存起来
    out_file = open(q_path,'wb')
    pickle.dump(abstract_list,out_file,True)

def filter_sent(sent_tokens,filter_val):
    "根据句子中的实体数，筛选在构建图结构时，要保留的句子"
    tmp_sents = []
    for sent in sent_tokens:
        finder = NgramEntityFinder(sent)
        enti_tokens = finder.extract_entity()
        if len(enti_tokens) >= filter_val:
            tmp_sents.append(sent)
    return tmp_sents

#text => sentences => graph => calculate => scores
def ExtractSentence(text,k):
    "根据文本内容获得句子重要性排名"
    print('开始句子重要性排名')

    sent_tokens = nlp.sent_tokenize(text)

    #可以加入限制条件，如果句子中的实体数少于阈值则放弃这个句子，等等，待扩展
    sent_tokens = filter_sent(sent_tokens,1)

    #建图结构
    text_graph = graph_construct(sent_tokens)

    #这里pagerank有三种，一种是正常的pg，一种是利用numpy还有一种就是下面的利用scipy的稀疏矩阵
    print('start to calculate')
    #cal_gr_page_rank = nx.pagerank(text_graph,weight='weight')
    cal_gr_page_rank = nx.pagerank_scipy(text_graph)
    print('ended')

    #按照最后的score得分进行排序，获得前K个，待扩展，使之取不超250个词的句子
    sents = sorted(cal_gr_page_rank,key = cal_gr_page_rank.get, reverse=True)

    kth = get_sum_sents(sents,250)
    #topK
    return ' '.join(sents[:kth])

def get_sum_sents(sents,limit_num):
    "对于按重要性排序的句子，获得不超过limit_num词数的尽量多的句子"
    total_num = 0
    idx = 0
    while(total_num <= limit_num and idx < len(sents)):
        total_num += len(nlp.word_tokenize(sents[idx]))
        if (total_num > limit_num):
            break
        idx += 1
    return idx

#实际运行时，发现整个构建图结构才是最耗时的阶段，可以在这上面优化时间复杂度
def graph_construct(nodes):
    "构建text_rank_graph"
    print('构建text_graph')

    #利用networkx简历图结构，节点即传入的sentences
    text_graph = nx.Graph()
    text_graph.add_nodes_from(nodes)

    #这里没有对边进行筛选，假设任意两个句子都是有相似性的
    nodePairs = list(itertools.combinations(nodes,2))
    for pair in nodePairs:
        first_sent = pair[0]
        second_sent= pair[1]
        #weights = lDistance(first_sent,second_sent)
        weights = sent_sim(first_sent,second_sent)
        text_graph.add_edge(first_sent,second_sent,weight=weights)
    print('graph construction end.')

    return text_graph

#论文中提到的共现相似度，也可以用其他的方法，如lexrank中的词袋+余弦距离
def sent_sim(sent_1,sent_2):
    sent_1_tokens = nlp.word_tokenize(sent_1)
    sent_2_tokens = nlp.word_tokenize(sent_2)

    #交集即为共现的词语
    sim_set = set(sent_1_tokens) & set(sent_2_tokens)
    num_up = len(sim_set)
    num_down = math.log(len(sent_1_tokens)) + math.log(len(sent_2_tokens))

    return num_up * 1. / num_down

'''
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
'''

if __name__ == "__main__":
    #get_abstract(filter_quesiton,filter_abstract,3)
    get_abstract(duc_question,duc_abstract,3)
