#!/usr/bin/python3
#coding=utf-8

import re
import pickle
#import sys
#sys.path.append("../code")
#import insummer
#from insummer.common_type import Question,Answer
#from insummer.read_conf import config

def get_topic(topic_path,test_path):
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
                str_list += line.rstrip()
        infile.close()
    print("开始抽取topic内容...")
    topic_str_list = topic_re.findall(str_list)
    
    for idx,item in enumerate(topic_str_list):
        topic_num = num_re.findall(item)[0]
        print(topic_num)

if __name__ == "__main__":
    topic_path = '/home/charch/gitwork/insummer/duc/duc_data/duc2007_topics.sgml'
    test_path = '/home/charch/gitwork/insummer/duc/duc_data/duc2007_testdocs/main/'
    get_topic(topic_path,test_path)
