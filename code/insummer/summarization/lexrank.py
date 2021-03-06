#!/usr/bin/python3
#coding=utf-8

'''
LexRank类
'''

from .summarizer import abstract_summarizer,ya_summarizer
from .tfidf import TFIDF
from ..common_type import Question,Answer
from ..read_conf import config
from ..util import NLP
from ..query_expansion.entity_finder import NgramEntityFinder
from math import log
from numpy import dot
from numpy.linalg import norm
import networkx as nx

data_conf = config('/home/lavi/project/insummer/conf/question.conf')

nlp = NLP()

class LexRank(abstract_summarizer):
    '''
    tfidf matrix => graph => pagerank => lexrank scores
    '''

    def __init__(self,q,words):
        #abstract_summarizer.__init__(self)
        self.__question = q
        self.words_limit = words
        print(q.get_author())

    #两个抽象方法，extract(self) evaluation(self,result)

    def extract(self):
        '''根据问题得到lexrankscore高的句子'''

        title_text = self.__question.get_title()
        answer_text = self.__question.get_nbest_content()

        print('句子重要性排名，开始分句..')
        self.nlp = NLP()

        sent_tokens = self.nlp.sent_tokenize(answer_text)

        print('获得句子列表，开始计算tfidf..')

        self.N = len(sent_tokens)
        self.tfidf = TFIDF(sent_tokens).matrix

        print('获得tfidf矩阵，开始构建图结构..')

        #这里用index来表示句子，方便找到tfidf值
        nodes = [idx for idx in range(self.N)]

        self.lex_graph = nx.Graph()
        self.lex_graph.add_nodes_from(nodes)

        #可以itertools创建组合数，或者直接循环加边
        #nodepairs = list(itertools.combinations(nodes,2))
        for i in range(self.N):
            for j in range(self.N):
                sim = self.get_cos(self.tfidf[i],self.tfidf[j])
                self.lex_graph.add_edge(i,j,weight=sim)

        print('图构建完成，开始计算lexrankscore..')

        cal_lexrank = nx.pagerank(self.lex_graph)

        print('计算完成，开始摘要..')

        orders = sorted(cal_lexrank,key=cal_lexrank.get,reverse=True)

        k_th = self.get_sum_sents(sent_tokens,orders)

        str_tmp_list = []
        for sidx in range(k_th):
            str_tmp = sent_tokens[orders[sidx]]
            str_tmp += '[%.4f]'%(cal_lexrank[sidx])
            str_tmp_list.append(str_tmp)
        for i in str_tmp_list:
            print(i)

        self.abstrct_text = ' '.join([sent_tokens[orders[ith]] for ith in range(k_th)])

        print('摘要完成..')

        #之后就是根据question标题，将abstract内容输出到指定位置，然后ROUGE了
        filename = self.__question.get_author()
        if filename[-1] == '/':
            filename = filename[:-1]
        sum_path = data_conf['lexrank_sum'] + filename
        with open(sum_path,'w') as sum_file:
            sum_file.write(self.abstrct_text)
        sum_file.close()

        #因为pyrouge接收的是路径，所以返回路径即可
        print(sum_path)
        return sum_path

    #def evaluation(self,result):
    #    '''ROUGE评测'''
    #    print(result)

    def abstract_output(self,result):
        '''根据question输出ab'''
        print('successfully.')
        #根据加入的文件名，输出到指定路径


    def get_sum_sents(self,sents,orders):
        '''根据index和scores找出最大k个句子'''

        total_num = 0
        idx = 0
        
        while(total_num <= self.words_limit and idx < len(sents)):
            total_num += len(self.nlp.word_tokenize(sents[orders[idx]]))
            if (total_num > self.words_limit):
                break
            idx += 1
        
        return idx

    
    def get_cos(self,vec1,vec2):
        '''计算两个句子的余弦相似度'''

        return dot(vec1,vec2) / (norm(vec1) * norm(vec2))
        
as_res = "/home/lavi/project/insummer/as_corpus/as_res/"        
class SPLexRank(ya_summarizer):
    '''
    tfidf matrix => graph => pagerank => lexrank scores
    '''

    def __init__(self,q,words):
        #abstract_summarizer.__init__(self)
        self.question = q
        self.words_limit = words
        print(q.get_author())

        nbest_total_words = 0
        nbest = q.get_nbest()
        for ans in nbest:
            content = ans.get_content()
            nbest_total_words += nlp.sentence_length(content)

        self.word_limit = min(int(nbest_total_words/3),150)
        print("词数限制",self.word_limit)    
        
        print("文章题目",self.question.get_title())


    #两个抽象方法，extract(self) evaluation(self,result)

    def extract(self):
        '''根据问题得到lexrankscore高的句子'''

        title_text = self.question.get_title()
        answer_text = self.question.get_nbest_content()

        print('句子重要性排名，开始分句..')
        self.nlp = NLP()

        sent_tokens = self.nlp.sent_tokenize(answer_text)

        print('获得句子列表，开始计算tfidf..')

        self.N = len(sent_tokens)
        self.tfidf = TFIDF(sent_tokens).matrix

        print('获得tfidf矩阵，开始构建图结构..')

        #这里用index来表示句子，方便找到tfidf值
        nodes = [idx for idx in range(self.N)]

        self.lex_graph = nx.Graph()
        self.lex_graph.add_nodes_from(nodes)

        #可以itertools创建组合数，或者直接循环加边
        #nodepairs = list(itertools.combinations(nodes,2))
        for i in range(self.N):
            for j in range(self.N):
                sim = self.get_cos(self.tfidf[i],self.tfidf[j])
                self.lex_graph.add_edge(i,j,weight=sim)

        print('图构建完成，开始计算lexrankscore..')

        cal_lexrank = nx.pagerank(self.lex_graph)

        print('计算完成，开始摘要..')

        orders = sorted(cal_lexrank,key=cal_lexrank.get,reverse=True)

        k_th = self.get_sum_sents(sent_tokens,orders)

        str_tmp_list = []
        for sidx in range(k_th):
            str_tmp = sent_tokens[orders[sidx]]
            str_tmp += '[%.4f]'%(cal_lexrank[sidx])
            str_tmp_list.append(str_tmp)
        for i in str_tmp_list:
            print(i)

        self.abstrct_text = ' '.join([sent_tokens[orders[ith]] for ith in range(k_th)])

        print('摘要完成..')

        #之后就是根据question标题，将abstract内容输出到指定位置，然后rouge了
        print("写入文件")
        wp = self.question.get_author()
        fname = as_res+wp.split("|")[0]+".res"
        print(fname)
        f = open(fname,"w")
        f.write(self.abstrct_text)
        f.close()
        return fname  

        
    #def evaluation(self,result):
    #    '''ROUGE评测'''
    #    print(result)

    def abstract_output(self,result):
        '''根据question输出ab'''
        print('successfully.')
        #根据加入的文件名，输出到指定路径


    def get_sum_sents(self,sents,orders):
        '''根据index和scores找出最大k个句子'''

        total_num = 0
        idx = 0
        
        while(total_num <= self.words_limit and idx < len(sents)):
            total_num += len(self.nlp.word_tokenize(sents[orders[idx]]))
            if (total_num > self.words_limit):
                break
            idx += 1
        
        return idx

    
    def get_cos(self,vec1,vec2):
        '''计算两个句子的余弦相似度'''

        return dot(vec1,vec2) / (norm(vec1) * norm(vec2))

