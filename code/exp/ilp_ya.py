#!/usr/bin/python3

'''
yahoo answer 摘要
'''

import sys
sys.path.append("..")
import insummer

import logging
from optparse import OptionParser 

from insummer.summarization.ilp import sparse_ilp as SI
from insummer.common_type import Question,Answer

as_dir = "/home/lavi/project/insummer/as_corpus/all/"
as_data = "/home/lavi/project/insummer/as_corpus/as_data/"
as_sum = "/home/lavi/project/insummer/as_corpus/as_sum/"
as_res = "/home/lavi/project/insummer/as_corpus/as_res/"
#先找到所有的文件名
import os
all_fnames = []
for fname in os.listdir(as_dir):
    num = fname[:-4]
    all_fnames.append(num)


import re,sys
#建立问句和答案的类

def build_questions():

    def replace_tag(l,tag):
        a = "<%s>"%(tag)
        b = "</%s>"%(tag)
        l = l.replace(a,"")
        l = l.replace(b,"")
        return l
        
    questions = []
    #对于每个文件名先开一下问题
    for fname in all_fnames:
        qfile = open(as_data+fname+".questions")
        author = fname + "|" + qfile.readline()

        title = ""
        content = ""
        nbest = []
        for line in qfile:
            if len(line)<=2:
                continue

            line = line.strip()
            #正式读
            if line.startswith("<subject>"):
                line = replace_tag(line,"subject")
                title = line
                
            elif line.startswith("<answer_item>"):
                line = replace_tag(line,"answer_item")
                manswer = Answer(line)
                nbest.append(manswer)
                
            elif line.startswith("<content>"):
                line = replace_tag(line,"content")
                content = line
                
            else:
                print("error",line,fname)

        q = Question(title=title+" "+content,content=content,best="",nbest=nbest,author=author)
        if len(nbest) == 0 :
            print(error,fname,title)
            sys.exit(1)
        questions.append(q)
        
    return questions

def exp(questions,qnum):
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        q.clean()
        ose = SI(q,100)

        result = ose.extract()
        print("写文件地址",result)
        ose.evaluation(result,"silp")
        print(100*"=")
    
if __name__ == '__main__':
    print(__doc__)
    questions = build_questions()

    exp(questions,len(questions))
    #exp(questions,45)

    print("问题总数",len(all_fnames))

    

    

    

        
