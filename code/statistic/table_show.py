#!/usr/bin/python3
#coding=utf-8

'''
这个主要是将抽取的语料与duc语料的整体统计特征做一个直观的输出比较，
整体代码糙的不行，全赖问题结构固定，先这么将就着看吧。
'''

import pickle
import sys

from question_table import question_table
sys.path.append('..')
from insummer.read_conf import config

question_conf = config('../../conf/question.conf')

fil_path = question_conf['filter_statistic']
duc_path = question_conf['duc_statistic']

infile = open(fil_path,'rb')
fil_table = pickle.load(infile)

infile = open(duc_path,'rb')
duc_table = pickle.load(infile)

def get_total_avg(duc_list,isavg,nq):
    qa_total = 0
    entitle_total = 0
    wdtitle_total = 0
    enanser_total = 0
    wdanser_total = 0
    sent_total = 0
    for qt in duc_list:
        qa_total += qt.qa_num
        entitle_total += qt.te_num
        wdtitle_total += qt.tw_num
        enanser_total += qt.an_enti
        wdanser_total += qt.an_word
        sent_total += qt.an_sent
    if isavg:
        return 1.*entitle_total/nq,1.*wdtitle_total/nq,1.*sent_total/qa_total,1.*enanser_total/qa_total,1.*wdanser_total/qa_total,1.*enanser_total/sent_total,1.*wdanser_total/sent_total
    else:
        return qa_total,entitle_total,wdtitle_total,enanser_total,wdanser_total,sent_total

def output_table(tables):
    '''
    for idx,qt in enumerate(tables):
        print("问题：%s"%qt.question_author)
        print("实体总数：%s   单词总数：%s   答案总数：%s"%(qt.get_question()))
        print("该问题标题  实体数：%s   单词数：%s"%(qt.te_num,qt.tw_num))
        print("该问题答案  总实体数：%s 总单词数：%s  平均句子数：%s  平均实体数：%s  平均单词数：%s"%(qt.an_enti,qt.an_word,qt.an_sent*1./qt.qa_num,qt.an_enti*1./qt.qa_num,qt.an_word*1./qt.qa_num))
        print("该问题答案中 每句平均实体数：%s  每句平均单词数：%s "%(qt.an_enti*1. / qt.an_sent,qt.an_word*1. / qt.an_sent))
        print("================================================================================")
    '''
    print("--------------------------------------------------------------")
    print("总问题数：%s"%len(tables))
    print("总答案数：%s 标题总实体数：%s 标题总单词数：%s 答案总实体数：%s 答案总单词数：%s 答案总句子数：%s "%(get_total_avg(tables,False,len(tables))))
    print("标题=>平均实体数：%0.4f 平均单词数：%0.4f  答案=>平均句子数：%0.4f 平均实体数：%0.4f 平均单词数：%0.4f  句子=>平均实体数：%0.4f 平均单词数：%0.4f"%(get_total_avg(tables,True,len(tables))))
    print("--------------------------------------------------------------")


if __name__ == "__main__":
    output_table(duc_table)
    output_table(fil_table)
