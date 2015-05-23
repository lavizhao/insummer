#!/usr/bin/python3

import json
from pprint import pprint

import sys
sys.path.append("..")
import insummer
from insummer.util import NLP

nlp = NLP()

#存储数据位置
indx_dir = "/home/lavi/project/insummer/index"


#产生问题的序对，用yield写的
def gen_qa():
    source_dir = "/home/lavi/project/insummer/question_retrival/computers.json"
    count = 0
    qnum = 0
    
    #开文件
    f = open(source_dir)

    questions = []
    title = ""

    for line in f:
        line = line.strip()
        if line[-1] == ",":
            line = line[:-1]

        js = json.loads(line)
        if "subject" in js:
            title = js["subject"]
            if len(title) > 3:
                qnum += 1
            if count != 0 :
                pass
                #qstr = json.dumps(questions)
                '''
                print("title",title.strip())
                for indx,q in enumerate(questions):
                    print("indx",indx,q.strip())
                print(100*"=")
                questions = []
                '''

        elif "content" in js:
            cont = js["content"]
            #cont = nlp.remove_tag(cont)
            #questions.append(cont)
            

        if qnum % 3000 == 0:
            print("qnum",qnum)
        count += 1
        if count % 10000 == 0:
            print("line,count",count/1000000,"M")

#临时存储question的        
class tquestion:
    def __init__(self,title,content,best,nbest):
        self.title = title
        self.content = content
        self.best = best
        self.nbest = nbest

    def print(self):
        print("title===>",self.title)
        print("content===>",self.content)
        print("best===>",self.best)
        for indx,q in enumerate(self.nbest):
            print("indx",indx,"===>",q)

        print(100*"=")
        
def gen_manner():
    source_dir = "/home/lavi/project/insummer/question_retrival/manner.xml"
                
    f = open(source_dir)

    qnum = 0
    nbest = []
    title = ""
    best = ""
    content = ""

    def contains(line,tags):
        for tag in tags:
            if line.startswith(tag):
                return True

        return False

    def replace(line,tag):
        line = line.replace("<%s>"%tag,"")
        line = line.replace("</%s>"%tag,"")
        return line.strip()
        
    unused_tags = ["<ystfeed>","</ystfeed>","<uri>","<yid>","<best_yid>","</nbestanswers>","<cat>","<maincat>","<subcat>"]
    for line in f:
        if line.startswith("<?xml version='1.0' encoding='UTF-8'?>"):
            pass
        elif contains(line,unused_tags):
            pass

        elif line.startswith("<vespaadd><document type=\"wisdom\">"):
            nbest = []
            title = ""
            best = ""
            content = ""

        elif line.startswith("</document></vespaadd>"):
            tq = tquestion(title=title,content=content,best=best,nbest=nbest)
            yield tq
            
        elif line.startswith("<subject>"):
            title = replace(line,"subject")

        elif line.startswith("<content>"):
            content = replace(line,"content")

        elif line.startswith("<bestanswer>"):
            best = replace(line,"bestanswer")

        elif line.startswith("<nbestanswers>"):
            line = replace(line,"nbestanswers")
            line = replace(line,"answer_item")
            line = nlp.remove_tag(line)
            nbest.append(line)

        elif line.startswith("<answer_item>"):
            line = replace(line,"answer_item")
            line = nlp.remove_tag(line)
            nbest.append(line)

        else:
            print("error")
            sys.exit(1)
        
#import whoosh
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT,ID,STORED
from whoosh.qparser import QueryParser

def write_indx():
    index_dir = "/home/lavi/project/insummer/index"
    schema = Schema(title=TEXT(stored=True),content=STORED,best=STORED,nbest=STORED)
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    count = 0
    for tq in gen_manner() :
        nbest_js = json.dumps(tq.nbest)
        writer.add_document(title=tq.title,content=tq.content,best=tq.best,nbest=nbest_js)
        count += 1
        if count % 1000 == 0:
            print(count/1000,"K")

    writer.commit()

            
if __name__ == '__main__':
    write_indx()
