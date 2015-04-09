#!/usr/bin/python3
#coding=utf-8

from datetime import datetime
import itertools
from numpy import *
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

#filter_path = question_conf['filter_qa']
duc_path = question_conf['duc_question']

#摘要保存路径要和textrank区别开，同时为了ROUGE不能简单地用pickle存储了
lexrank_path = question_conf['lexrank_sum']

nlp = NLP()

#获得问题
#filter_file = open(filter_path,'rb')
#filter_question = pickle.load(filter_file)
duc_file = open(duc_path,'rb')
duc_question = pickle.load(duc_file)

'''
    # 建图的时候需要计算这个问题的各个句子的tf idf啊喂
    # 然后根据tf idf 计算所有句子（整个图）的邻接矩阵，构造图呀！
    # 所以：得到某个问题，得到答案文本，词表，分句，分词，对句子中的词计算tf idf
    # 然后：任意两个句子的相似度计算，然后建图，就是pagerank啦！
'''

def lexrank(questions,q_path):
    "LEXRANK方法提取摘要"
    
    abstract_list = []
    
    for idx,s_question in enumerate(questions):
        print('处理第 %s 个问题'%idx)
        start_time = datetime.now()
        
        #获得这个问题的答案文本
        title = s_question.get_title()
        answer_text = s_question.get_nbest_content()
        
        #对于每个答案要创建一个摘要类，利用标题和答案初始化
        #这个对于最后的ROUGE需要单个存储
        temp_abstract = abstract_type(title,answer_text)

        #对某一个答案抽取topK个句子，满足再多一个就超过词限制
        abstract_text = ExtractSentence(answer_text)

        #for rouge save the single summarization.
        filename = s_question.get_author()
        if filename[-1] == '/':
            filename = filename[:-1]
        sum_path = lexrank_path + filename
        with open(sum_path,'w') as sum_file:
            sum_file.write(abstract_text)
            print('abstract for %s is wrote..'%filename)
        sum_file.close()

        temp_abstract.update_abstract(abstract_text)
        abstract_list.append(temp_abstract)

        times = datetime.now() - start_time
        print("长度：%s 用时：%s \n 摘要：%s"%(len(answer_text),times,abstract_text))

    #out_file = open(q_path,'wb')
    #pickle.dump(abstract_list,out_file,True)


def ExtractSentence(answer_text):
    "Lexrank alg."

    print("句子重要性排名，开始分句...")
    
    #分句，获得类'docs'列表
    sent_tokens = nlp.sent_tokenize(answer_text)

    print("获得句子列表，开始计算tfidf...")

    #统计出词，句子的词频逆文档等
    tfidf_matrix,sent_N,word_N = get_tfidf(sent_tokens)

    print("获得tfidf矩阵，开始构建图...")

    #这里用index来表示句子，因为后面计算不用句子的文本信息了，同时也方便在矩阵中找
    nodes = [idx for idx in range(word_N)]
    lex_graph = nx.Graph()
    lex_graph.add_nodes_from(nodes)

    #之后建图或者邻接矩阵都可以，i，j间的相似度就是tfidf[i]和tfidf[j]的余弦相似度
    #nodepairs = list(itertools.combinations(nodes,2))
    for i in range(sent_N):
        for j in range(sent_N):
            #i,j和sents列表对应的，就用这个建图也是可以的
            sim = get_cos(tfidf_matrix[i],tfidf_matrix[j])
            lex_graph.add_edge(i,j,weight=sim)

    print("图构建完成，开始迭代计算...")

    #开始迭代计算至收敛
    cal_lex_rank = nx.pagerank(lex_graph)

    print("计算完成，开始摘要...")

    orders = sorted(cal_lex_rank,key = cal_lex_rank.get,reverse=True)

    kth = get_sum_sents(sent_tokens,orders,250)

    str_tmp_list = []
    for sidx in range(kth):
        str_tmp = sent_tokens[orders[sidx]]
        str_tmp += '[%.4f]'%(cal_lex_rank[sidx])
        str_tmp_list.append(str_tmp)
    print_score(str_tmp_list)

    return ' '.join([sent_tokens[orders[ith]] for ith in range(kth)])
    #for node, pagerankVal in pr.items():
    #    print("%d,%.4f"%(node,pagerankVal))

def print_score(sen_list):
    for i in sen_list:
        print(i)

def get_sum_sents(sents,orders,limit_num):
    "找到不超limit的最多的句子数"
    total_num = 0
    idx = 0
    while(total_num <= limit_num and idx < len(sents)):
        total_num += len(nlp.word_tokenize(sents[orders[idx]]))
        if (total_num > limit_num):
            break
        idx += 1
    return idx


def get_tfidf(sents):
    "根据句子列表，获得句子和词的词频等信息矩阵"
    
    #获得词表和句子数，词表大小
    word_set = get_word_set(sents)
    sent_N = len(sents)
    word_N = len(word_set)

    #根据词表建立tfidf矩阵，行句子，列词
    tfidf_matrix = zeros((sent_N,word_N))
    for d in range(sent_N):
        tfidf_matrix[d,:] = make_vector(sents[d],word_N,word_set)

    #转换 tf => tf-idf
    tfidf_matrix = matrix_transform(tfidf_matrix,word_N)
    
    return tfidf_matrix,sent_N,word_N
            

def get_word_set(sents):
    "根据文章（句子）列表，获得整个的词表"
    
    word_set = set()
    for sent in sents:
        temp_set = set(nlp.word_tokenize(sent))
        word_set = word_set | temp_set
    return list(word_set)


def make_vector(sent,word_N,word_set):
    "将某个句子转换成词袋向量"

    vector = zeros(word_N)
    for word in nlp.word_tokenize(sent):
        #利用数组中的词找到index
        try: vector[word_set.index(word)] += 1
        except ValueError:continue
    return vector


def get_cos(vec1,vec2):
    "计算余弦相似度"
    
    return dot(vec1,vec2) / (linalg.norm(vec1) * linalg.norm(vec2))


def matrix_transform(temp_matrix,word_N):
    "将tf矩阵转换成tfidf矩阵"

    for col in range(word_N):
        count = float(temp_matrix.sum(axis=0)[col])
        idf = log(word_N / count)
        temp_matrix[:,col] *= idf

    return temp_matrix


if __name__ == "__main__":
    lexrank(duc_question,'temp')
