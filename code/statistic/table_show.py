#!/usr/bin/python3
#coding=utf-8

import pickle
import sys

from question_table import question_table
sys.path.append('..')
from insummer.read_conf import config

question_conf = config('../../conf/question.conf')

fil_path = question_conf['filter_statistic']
duc_path = question_conf['duc_statistic']

#infile = open(fil_path,'rb')
#fil_table = pickle.load(infile)
infile = open(duc_path,'rb')
duc_table = pickle.load(infile)

def get_total_avg(duc_list):
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
    return qa_total,entitle_total,wdtitle_total,enanser_total,wdanser_total,sent_total

if __name__ == "__main__":
    for idx,qt in enumerate(duc_table):
        print("问题：%s  实体总数：%s   单词总数：%s   答案总数：%s"%(qt.question_author,qt.qe_num,qt.qw_num,qt.qa_num))
        print("该问题标题  实体数：%s   单词数：%s"%(qt.te_num,qt.tw_num))
        print("该问题答案  总实体数：%s 总单词数：%s  平均句子数：%s  平均实体数：%s  平均单词数：%s"%(qt.an_enti,qt.an_word,qt.an_sent*1./qt.qa_num,qt.an_enti*1./qt.qa_num,qt.an_word*1./qt.qa_num))
        print("================================================================================")
    print("--------------------------------------------------------------")
    print("总问题数：%s"%len(duc_table))
    print("总答案数：%s 标题总实体数：%s 标题总单词数：%s 答案总实体数：%s 答案总单词数：%s 答案总句子数：%s "%(get_total_avg(duc_table)))
    print("--------------------------------------------------------------")
