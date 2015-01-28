#!/usr/bin/python3
#coding=utf-8

'''
TextRank类
'''

from .summarizer import abstract_summarizer
from ..common_type import Question,Answer
from ..read_conf import config
from ..util import NLP
from ..query_expansion.entity_finder import NgramEntityFinder
from math import log
import itertools
import networkx as nx

class TextRank(abstract_summarizer):
    '''
    text => sents => graph => pagerank => textrank scores
    '''

    #init:已知__question/words_limit
    def __init__(self):
        abstract_summarizer.__init__(self)

    #两个抽象方法，extract(self) evaluation(self,result)
    
    def extract(self):
        '''根据文本内容对句子重要性排名，同时根据limit抽取前K个句子'''

        print('开始句子重要性排名')
        
        #得在question里存放对应的文件名..
        
        title_text = self.__question.get_title()
        answer_text = self.get_nbest_content()

        self.nlp = NLP()
        
        #分句，在textrank中，这也是图结构的nodes
        sent_tokens = nlp.sent_tokenize(answer_text)

        #根据文本条件筛选句子，可扩展
        #sent_tokens = filter_sent(sent_tokens,2)

        #建图结构
        self.graph_construct(sent_tokens)

        #开始textrank
        print('开始计算textrank scores')

        #pagerank:1-pagerank(..) 2-pagerank_numpy(..) 3-pagerank_scipy(..)
        cal_pagerank = nx.pagerank(self.__text_graph)

        print('开始摘要..')

        #最后按照score排序，取不超limit的前k个句子
        sents = sorted(cal_pagerank,key = cal_pagerank.get,reverse = True)

        k_th = self.get_sum_sents(sents)

        self.__abstract_text = ' '.join(sents[:k_th])
        
        print('摘要完成..')

        #之后就是根据question标题，将abstract内容输出到指定位置，然后rouge了
        #待续

    def evalutaion(self):
        '''ROUGE评测'''

        abstract_output()

        #调用pyrouge

    def abstract_output(self):
        '''根据question输出ab'''

        #根据加入的文件名，输出到指定路径


    def graph_construct(self,nodes):
        '''创建图结构'''
        print('开始创建图结构')

        self.__text_graph = nx.Graph()
        self.__text_graph.add_nodes_from(nodes)

        #这里没有对边进行筛选，假设了任意两边有相似性
        nodepairs = list(itertools.combinations(nodes,2))

        for pair in nodepairs:

            first_sent = pair[0]
            second_sent = pair[1]

            #权重，这里选择共现词，可以更改
            weights = self.sent_sim(first_sent,second_sent)

            self.__text_graph.add_edge(first_sent,second_sent,weight=weights)

        print('建图完成..')


    def filter_sent(self,sent_tokens,filter_val):
        '''根据给定的条件筛选句子'''
    
        temp_sents = []

        for sent in sent_tokens:

            finder = NgramEntityFinder(sent)
            entities = finder.extract_entity()

            if len(entities) >= filter_val:
                tmp_sents.append(sent)

        return temp_sents

    def sent_sim(self,sent_1,sent_2):
        '''计算两个句子之间的相似度'''

        sent_1_tokens = self.nlp.word_tokenize(sent_1)
        sent_2_tokens = self.nlp.wprd_tokenize(sent_2)
        
        #交集即为共现的词语
        sim_set = set(sent_1_tokens) & set(sent_2_tokens)
        
        num_up = len(sim_set)
        num_down = log(len(sent_1_tokens)) + log(len(sent_2_tokens))

        return num_up * 1. / num_down

    def get_sum_sents(self,sents):
        '''根据words_limit筛选出k个句子'''

        total_num = 0
        idx = 0

        while(total_num <= self.words_limit and idx < len(sents)):
            total_num += len(self.nlp.word_tokenize(sents[idx]))
            if (total_num > self.words_limit):
                break
            idx += 1

        return idx
