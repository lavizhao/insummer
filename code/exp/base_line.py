#!/usr/bin/python3
#coding=utf-8

'''
**************************
 * File Name :base_line.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

import insummer

from insummer.query_expansion.entity_finder import NgramEntityFinder
from insummer.summarization.lexrank import LexRank
from insummer.summarization.textrank import TextRank
finder = NgramEntityFinder

import pickle
import data
import logging
from optparse import OptionParser

def exp(questions,qnum,method):
    for i in range(qnum):
        print('问题 : %s'%(i))
        q = questions[i]
        
        lexer = LexRank(q,250)
        result = lexer.extract()
        lexer.evaluation(result,'lex')

if __name__ == "__main__":
    print(__doc__)

    #parser = OptionParser()
    #parser.add_option('-d','--data',dest='data',help='选择数据集')
    #parser.add_option('-m','--method',dest='method',help='算法选择')
    #(options,args) = parser.parse_args()

    print('loading the data..')
    duc_question = pickle.load(open('/home/lavi/project/insummer/question_data/duc_question.pkl','rb'))

    #method = options.method
    
    exp(duc_question,4,'lex')
