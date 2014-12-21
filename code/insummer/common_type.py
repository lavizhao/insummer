#!/usr/bin/python3
#coding=utf-8

'''
这个文件的主要作用是定义一些常见的数据结构
'''

from .util import NLP
import sys

nlp = NLP()

#问题类,一个问题通常有
#1.标题 title
#2.内容,描述, content
#3.最佳答案,best
#4.所有答案,nbest
#5.作者,author
#6.答案数目,answer_count
#六个部分组成
class Question:
    def __init__(self,title,content,best,nbest,author="",answer_count=0):
        self.__title = nlp.remove_tag(title)
        self.__content = nlp.remove_tag(content)
        self.__best = best
        self.__nbest = nbest
        self.__author = author
        self.__count = answer_count
        self.type_name = "Question"

    def get_author(self):
        return self.__author

    def get_title(self):
        return self.__title

    def get_best(self):
        return self.__best

    #得到答案数目
    def get_count(self):
        return len(self.__nbest)

    #得到所有答案的内容
    def get_nbest_content(self):
        target = ""
        indx = 0
        for i in self.__nbest:
            target += "%s,%s\n"%(indx,i.get_content())
            indx += 1

        return target


    def get_nbest(self):
        return self.__nbest
        
    def get_word_counts(self):
        result = 0

        #加上title的单词数
        result += len(self.__title.split())

        #加上best的单词数
        result += len(self.__best.split())

        #加上nbest的单词数
        for one_nbest in self.__nbest:
            result += len(one_nbest.get_content().split())

        return result

    def get_title_words(self):
        return len(self.__title.split())
        
    def print(self):
        print(20*"=")
        print("title",self.__title)
        print("content",self.__content)
        print("best",self.__best)
        for i,indx in enumerate(self.__nbest):
            print("====",i,indx)
        print("author",self.__author)
        print("count",self.__count)
        print(20*"=")
        
#答案类,注:这里的答案是指一条答案, 不是指其他的语义, 是Question里面的一个组成部分
#包含以下几个部分:
#1.答案内容
#2.支持反对数目
#3.作者hash值
class Answer:
    def __init__(self,sentence,support=0,oppose=0,author=""):
        self.type_name = "Answer"
        self.__content = nlp.remove_tag(sentence)
        self.__support = support
        self.__oppose = oppose
        self.__author = author

    #得到内容,即这个答案
    def get_content(self):
        return self.__content

    def __str__(self):
        return "type:%s content:%s support:%s oppose:%s author:%s"%(self.type_name,self.__content\
                                 ,self.__support,self.__oppose,self.__author)


class NaiveQuestion(Question):
    def __init__(self,title,entity):
        Question.__init__(self,title,"","",None,None,None)
        self.__entity = entity

    def get_word_counts(self):
        return len(self.get_title().split())

    def get_entity(self):
        return self.__entity
        
    def print(self):
        print("title",self.get_title())
        st = ' '.join(self.__entity)
        print("entity",st)

    def set_entity(self,entity):
        self.__entity = entity
