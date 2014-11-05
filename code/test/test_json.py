#!/usr/bin/python3

'''
这个文件主要的作用是实验python3如何操作json文件
'''

import sys
sys.path.append("..")
import insummer

from insummer.read_conf import config
from insummer.common_type import Question,Answer

import json

def test1():
    conf = config("../../conf/question.conf")

    f = open(conf["computer_pos"])

    indx = 0

    title = ""
    nbest = []
    answer_count = -1
    author = ""

    questions = []
    
    line = f.readline()

    question_indx = 0
    
    while len(line) > 0 :

        #先去除line两边的空格和最后结尾的逗号
        line = line.strip()

        if line[-1] == ',':
            line = line[:-1]
            
        #把json都装载进来
        try:    
           line_json = json.loads(line)
        except:
            print(line)
            sys.exit(1)

        #判断是answer还是question
        if "answercount" in line_json:
            #是问题

            #先把上一个问题的存了
            #content为空,best空
            #如果nbest为空,说明还没有人回答过, 那么不处理
            if len(nbest) > 0:
                m_question = Question(title,"","",nbest,author,answer_count)
                #m_question.print()
                #questions.append(m_question)
                question_indx += 1
                if question_indx % 100 == 0:
                    print("question indx",question_indx)

            #重新计数
            if len(line_json["answercount"].strip()) > 0:
                answer_count = int(line_json["answercount"])
            else:
                answer_count = 0
            title,nbest,author = "",[],""

            #现在开始重新存
            title = line_json["subject"]
            

        elif "content" in line_json:
            content = line_json["content"]
            support = int(line_json["supportnum"])
            oppose = int(line_json["opposenum"])
            ans_author = line_json["answeruser"]
            
            emp_answer = Answer(content,support,oppose,ans_author)

            nbest.append(emp_answer)
            
        else:
            print("error")
            sys.exit(1)
            
        indx += 1
        line = f.readline()
        if indx %1000 == 0:
            print("indx",indx)

    m_question = Question(title,"","",nbest,author,answer_count)
    #m_question.print()
    #questions.append(m_question)
    #
    #for q in questions:
    #    q.print()
    
if __name__ == '__main__':
    print("开始")
    test1()
