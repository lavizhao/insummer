#!/usr/bin/python3
#coding=utf-8

import sys
import pickle

from question_table import question_table
sys.path.append("..")
import insummer
from insummer.read_conf import config
from insummer.util import NLP
from insummer.query_expansion.entity_finder import NgramEntityFinder

#获得两个问题集的路径信息，并读取
ques_conf = config('../../conf/question.conf')
filter_path = ques_conf['filter_qa']
duc_path = ques_conf['duc_question']

fil_spath = ques_conf['filter_statistic']
duc_spath = ques_conf['duc_statistic']

nlp = NLP()

finfile = open(filter_path,'rb')
fil_data = pickle.load(finfile)
dinfile = open(duc_path,'rb')
duc_data = pickle.load(dinfile)

def get_statistic(path,data):
    q_list = []
    for idx,f_question in enumerate(data):
        print("==>%s question.."%idx)
        q_no = "FQ%s"%idx
        tmp_table = question_table(q_no,f_question.get_author())

        title = f_question.get_title()
        sents = nlp.sent_tokenize(title)
        e_num = 0
        w_num = 0
        for sent in sents:
            finder = NgramEntityFinder(sent)
            tmp_enti = finder.extract_entity()
            e_num += len(tmp_enti)
            w_num += len(nlp.word_tokenize(sent))
        tmp_table.update_title(e_num,w_num)

        answers = f_question.get_nbest()
        a_num = len(answers)
        for idx,answer in enumerate(answers):
            e_num = 0
            w_num = 0
            content = answer.get_content()
            sents = nlp.sent_tokenize(content)
            s_num = len(sents)
            for sent in sents:
                finder = NgramEntityFinder(sent)
                tmp_enti = finder.extract_entity()
                e_num += len(tmp_enti)
                w_num += len(nlp.word_tokenize(sent))
            tmp_table.update_answer(idx,s_num,e_num,w_num)
        print(a_num)
        tmp_table.update_question(a_num,w_num+tmp_table.tw_num,e_num+tmp_table.te_num)
        q_list.append(tmp_table)

    in_file = open(path,'wb')
    pickle.dump(q_list,in_file,True)

if __name__ == "__main__":
    print("开始处理filterquestion..")
    #get_statistic(fil_spath,fil_data)
    print("开始处理ducquestion..")
    get_statistic(duc_spath,duc_data)
