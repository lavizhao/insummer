#!/usr/bin/python3
#coding=utf-8

import re
import pickle
import sys
#sys.path.append("..")
#import insummer
#from insummer.common_type import Question,Answer
#from insummer.read_conf import config

#t_path = config('../../conf/question.conf')

def doc_to_answer(doc_path):
    answer_re = re.compile(r'''<TEXT>(.+?)</TEXT>''',re.DOTALL)
    p_re = re.compile(r'''<P>(.+?)</P>''',re.DOTALL)
    text_str = ''
    with open(doc_path,'r') as infile:
        for line in infile.readlines():
            if line != '\n':
                text_str += line
        infile.close()
    answer_part = answer_re.findall(text_str)[0]
    p_list = p_re.findall(answer_part)
    text_str = ''
    for idx,p_line in enumerate(p_list):
        #text_str += p_line.rstrip('\n')
        text_str += p_line.replace('\n',' ')
    return text_str

def get_topic(t_path):
    #REs for extract the topic items
    topic_re = re.compile(r'''<topic>(.+?)</topic>''',re.DOTALL)
    num_re = re.compile(r'''<num>(.+?)</num>''',re.DOTALL)
    title_re = re.compile(r'''<title>(.+?)</title>''',re.DOTALL)
    narr_re = re.compile(r'''<narr>(.+?)</narr>''',re.DOTALL)
    doc_re = re.compile(r'''<docs>(.+?)</docs>''',re.DOTALL)

    print("开始读取topic文档...")
    str_list = ''
    with open(topic_path,'r') as infile:
        for line in infile.readlines():
            if line != '\n':
                str_list += line
        infile.close()
    print("开始抽取topic内容...")
    topic_str_list = topic_re.findall(str_list)
    
    for idx,item in enumerate(topic_str_list):
        #doc_topic_dir:
        topic_dir_num = num_re.findall(item)[0].replace(' ','/')
        #question_title:
        topic_title = title_re.findall(item)[0]
        topic_narr = narr_re.findall(item)[0]
        #answer's document
        topic_docs = doc_re.findall(item)[0].split('\n')[1:-1]

        #construct the question:
        question_title = topic_title + topic_narr

        #construct the answer:
        for doc_t in topic_docs:
            doc_path = test_path + topic_dir_num + doc_t
            single_answer = doc_to_answer(doc_path)
            print(single_answer)
            break
        break


if __name__ == "__main__":
    topic_path = '/home/charch/gitwork/insummer/duc/duc_data/duc2007_topics.sgml'
    test_path = '/home/charch/gitwork/insummer/duc/duc_data/duc2007_testdocs/main'
    get_topic(topic_path)
