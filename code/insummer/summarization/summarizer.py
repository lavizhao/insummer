#!/usr/bin/python3
'''
说明:这里放着的就只是一个摘要的抽象类, 给看接口用的
'''
from abc import ABCMeta, abstractmethod
from ..read_conf import config

#Q是question类
#words是最长字数
class abstract_summarizer(metaclass=ABCMeta):
    def __init__(self,Q,words):
        self.question = Q
        self.words_limit = words

    def get_question(self):
        return self.question

    def get_words_limit(self):
        return self.words_limit

    #抽象方法
    #返回一个sentence的list, sentence的词数之和小于word_limit.
    #现在先这么写着,到时候再换
    @abstractmethod
    def extract(self):
        pass


