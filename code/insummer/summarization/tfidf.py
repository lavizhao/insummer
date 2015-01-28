#!/usr/bin/python3
#coding=utf-8

from numpy import zeros,log
from ..util import NLP


class TFIDF(object):
    '''
    根据分句内容，创建整个问题答案的tfidf矩阵
    '''

    def __init__(self,sents):
        '''根据句子列表初始化，词表，统计..'''

        self.sents = sents
        self.nlp = NLP()
        self.get_word_set()

        self.sent_num = len(self.sents)
        self.word_num = len(self.words)

        self.make_matrix()


    def get_word_set(self):
        '''根据sents获得词表'''

        self.words = set()

        for sent in self.sents:
            temp_set = set(self.nlp.word_tokenize(sent))
            self.words = self.words | temp_set
        
        #之后用到它的index，所以转换成list形式
        self.words = list(self.words)

        print('获得词表...')


    def make_matrix(self):
        '''构建邻接矩阵'''

        self.matrix = zeros((self.sent_num,self.word_num))
        
        for idx in range(self.sent_num):
            self.matrix[idx,:] = self.make_vector(self.sents[idx])

        for col in range(self.word_num):
            count = float(self.matrix.sum(axis=0)[col])
            idf = log(self.word_num / count)
            self.matrix[:,col] *= idf

    
    def make_vector(self,sent):
        '''统计单个句子信息'''

        vector = zeros(self.word_num)

        for word in self.nlp.word_tokenize(sent):
            vector[self.words.index(word)] += 1

        return vector
