#!/usr/bin/python3

import json
import sys
sys.path.append("..")
import insummer

#这个是只用了title的Question类,非常傻逼易用好用
from insummer.common_type import NaiveQuestion

from insummer.read_conf import config

from conceptnet5 import assoc_query
from conceptnet5 import query
from conceptnet5.query import AssertionFinder as Finder

#读数据,是个json群
def read_data(fname):

    questions = []
    
    f = open(fname)

    raw = f.readlines()

    for line in raw:
        if len(line) <= 0:
            continue

        line_json = json.loads(line)
        
        title = line_json["title"]
        entity = line_json["entity"]

        entity = entity.split(",")

        #建一个naive版本的question
        nq = NaiveQuestion(title,entity)

        questions.append(nq)

    return questions


if __name__ == '__main__':
    print("这个是测试语义扩展的")
    print("需要做的第一步是读取数据,建立一个比较虚假的quesion_list类")

    #注册表
    conf = config("../../conf/question.conf")

    #读数据
    questions = read_data(conf["title_qe_pos"])

    #装载spreading activation
    finder = Finder()
    dir1 = '/home/lavi/.conceptnet5/assoc/assoc-space-5.3'

    sa = assoc_query.AssocSpaceWrapper(dir1,finder)

    g = lambda x : x.startswith('/c/en')
    
    for question in questions:
        question.print()
        terms = question.get_entity()
        terms = [('/c/en/'+i,1.0) for i in terms]

        result = sa.expand_terms(terms)

        for term,weight in result:
            if term.startswith('/c/en'):
                print("%40s%40s"%(term[6:],weight))

        result1 = sa.associations(terms,limit=40)
    
        for term,weight in result1:
            if term.startswith('/c/en'):
                print("%40s%40s"%(term[6:],weight))


        print(40*"=")
        
