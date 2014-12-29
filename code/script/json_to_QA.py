#!/usr/bin/python3
#coding=utf-8

import json
import xml
import re
import optparse
import pickle
import sys
sys.path.append('..')
from optparse import OptionParser
import insummer
from insummer.common_type import Question,Answer
from insummer.read_conf import config
from insummer.util import NLP
from insummer.query_expansion.entity_finder import NgramEntityFinder

nlp = NLP()

#totally new extract functions
#infile需要读取的文件，outfile目标存储文件
#question是需要把文件存储的格式
#pass_filter满足条件的问题写入
def extract(infile,outfile,question_format,pass_filter=None,store_file=None):
    in_file = open(infile)
    out_file = open(outfile,'w')

    #idx是文件的行号
    idx,question_idx = 0,1
    title,nbest,answer_count,author = "",[],-1,""

    store = []

    line = in_file.readline()

    while len(line) > 0:
        #先去除line两边的空格和最后结尾的逗号
        line = line.strip()
        if line[-1] == ',':
            line = line[:-1]

        #解析json
        try:
            line_json = json.loads(line)
        except:
            print('error')
            print(line)
            print('index',idx)
            print('question_index',question_idx)
            sys.exit(1)

        #判断问题还是答案
        if "answercount" in line_json:
            #问题，先把上一个存了
            #如果nbest为空，每人回答，不处理
            if len(nbest) > 0:
                m_question = Question(title,"","",nbest,author,answer_count)

                #写！！！判断是否满足最小答案的要求，是否满足filter条件！
                if pass_filter(m_question):
                    question_idx += 1
                    out_file.write(question_format(m_question))
                    if store_file != None:
                        store.append(m_question)

                    if question_idx % 100 == 0:
                        print('question idx',question_idx)

            #重新计数
            if len(line_json['answercount'].strip()) > 0:
                answer_count = int(line_json['answercount'])
            else:
                answer_count = 0

            title,nbest,author = "",[],""

            title = line_json['subject']
            author = line_json['postuser']

        elif 'content' in line_json:
            content = line_json['content']
            support = int(line_json['supportnum'])
            oppose = int(line_json['opposenum'])
            ans_author = line_json['answeruser']

            emp_answer = Answer(content,support,oppose,ans_author)

            nbest.append(emp_answer)

        else:
            print('error')
            sys.exit(1)

        idx += 1
        line = in_file.readline()
        if idx % 10000 == 0:
            print('idx',idx)

    m_question = Question(title,"","",nbest,author,answer_count)
    if pass_filter(m_question):
        out_file.write(question_format(m_question))

    if store_file != None:
        t = open(store_file,'wb')
        pickle.dump(store,t,True)

#问题过滤函数，将满足：标题实体5-10，答案句子15-20，单词数彪过800的来！
def question_filter(question):
    T_E_N = 5
    A_S_N = 8
    S_W_N = 1000

    #title,each answer in nbest!
    #得到标题
    title = question.get_title()
    #得到问题答案数目
    answer_count = question.get_count()
    #得到所有答案的列表
    nbest = question.get_nbest()
    #得到每个答案 [i.get_content() for i in nbest]
    #nbest_content = question.get_nbest_content()

    title_sents = nlp.sent_tokenize(title)
    title_entity_num = 0
    for sent in title_sents:
        finder = NgramEntityFinder(sent)
        title_entity_num += len(finder.extract_entity())

    answer_avg_sents = 0
    answer_word_num = 0
    for idx_ans in nbest:
        answer_sents = nlp.sent_tokenize(idx_ans.get_content())
        answer_avg_sents += len(answer_sents)
        for sent in answer_sents:
            answer_word_num += len(nlp.word_tokenize(sent))

    answer_avg_sents = answer_avg_sents * 1. / answer_count

    if title_entity_num < T_E_N or answer_avg_sents < A_S_N or answer_word_num < S_W_N or answer_count < 5:
        return False
    else:
        return True

def extract_title_nbest(tquestion):
    return tquestion.get_title()+"\n"+ tquestion.get_nbest_content() + 20*"="+"\n"   

if __name__ == "__main__":
    question_conf = config('../../conf/question.conf')
    store_path = question_conf['filter_qa']
    extract(question_conf['new_question'],question_conf['title_nbest_pos'],extract_title_nbest,question_filter,store_path)
