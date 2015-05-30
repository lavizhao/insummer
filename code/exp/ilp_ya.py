#!/usr/bin/python3

'''
yahoo answer 摘要
'''

import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config


data_conf = config('../../conf/question.conf')

import logging
from optparse import OptionParser 

from insummer.summarization.ilp import sparse_ilp as SI
#from insummer.summarization.textrank import SPTextRank as TR
#from insummer.summarization.lexrank import SPLexRank as LR
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


def write_tofile(question,sent_list):
    wp = question.get_author()
    fname = as_res+wp.split("|")[0]+".res"
    f = open(fname,"w")
    for msent in sent_list:
        f.write(msent+" ")

    f.close()
    return fname  
    
    
def evaluation(result,flags,q):

    xml_file = open(data_conf['xml_path'],'w')

    author = q.get_author()
    fname = author.split("|")[0]

    #step1 xml开头
    xml_file.write('<ROUGE_EVAL version="1.5.5">\n')

    #step2 eval id => 这个写文件名，例如1.txt => 里面含有标准的摘要
    xml_file.write('<EVAL ID="' + fname + '">\n')

    #这个是我自己写的
    xml_file.write('<PEER-ROOT>\n')
    xml_file.write(as_res + '\n')
    xml_file.write('</PEER-ROOT>\n')


    #模型的，就是标准数据集
    xml_file.write('<MODEL-ROOT>\n')
    xml_file.write(as_sum + '\n')
    xml_file.write('</MODEL-ROOT>\n')

    #写文件的格式
    xml_file.write('<INPUT-FORMAT TYPE="SPL">\n')
    xml_file.write('</INPUT-FORMAT>\n')

    #这个是我自己的文件名
    sum_name = fname+".res"
    xml_file.write('<PEERS>\n')
    xml_file.write('<P ID="01">' + sum_name + '</P>\n')
    xml_file.write('</PEERS>\n')
    
    #这个是模型的
    xml_file.write('<MODELS>\n')
    xml_file.write("<M ID=\"A\">%s.sum</M>\n"%(fname))
    xml_file.write('</MODELS>\n')

    xml_file.write('</EVAL>')
    xml_file.write('</ROUGE_EVAL>')
    xml_file.close()

    options = ' -n 4 -w 1.2 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -a '
        
    score_path = data_conf['ROUGE_SCORE']+fname+"silp"
        
    exec_command = data_conf['ROUGE_PATH'] + ' -e ' + data_conf['rouge_data_path'] + options + ' -x ' + data_conf['xml_path'] + ' > ' + score_path

    os.system(exec_command)

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

    
def exp(questions,qnum,method):
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        q.clean()
        if method == "sip":
            ose = SI(q,100)
        else:
            pass

        '''
        elif method == "dum":
            ose = YA(q,100)
        elif method == "tr":
            ose = TR(q,100)
        elif method == "lr":
            ose = LR(q,100)
            
        else:
            print("没有选定指定方法")
            sys.exit(1)
        '''
        slist = ose.extract()
        wp = write_tofile(ose.get_question(),slist)
        evaluation(wp,"silp",ose.get_question())
        print(100*"=")


from optparse import OptionParser         
if __name__ == '__main__':
    print(__doc__)
    questions = build_questions()


    parser = OptionParser()  
    parser.add_option("-m", "--method", dest="method",help="方法")

    (options, args) = parser.parse_args()

    exp(questions,len(questions),options.method)
    #exp(questions,45)

    print("问题总数",len(all_fnames))

    

    

        
