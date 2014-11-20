#!/usr/bin/python3

'''
说明:这个文件是查询扩展类,主要负责查询扩展方面的工作
'''

from abc import ABCMeta, abstractmethod
from ..common_type import Question
from ..util import NLP
from .entity_finder import NgramEntityFinder

nlp = NLP()

#定义抽象类
#这个类是实体扩展的类,主要功能是
#1.给定question, 对其进行实体扩展
#2.将title扩展的实体与answer相比较
#3.能够换用不同的策略进行扩展

class abstract_entity_expansioner(metaclass=ABCMeta):
    def __init__(self,mquestion,entity_finder):
        assert mquestion.type_name == "Question"

        self.__question = mquestion

        #这个包含的是每个句子中的实体和句子
        #基本结构是[ (sentence(without tokenize) , [entity]  ) ]
        self.__sentence_entity = []

        self.__expand_entity = None

    
    def get_question(self):
        return self.__question

    def get_answers(self):
        return self.__question.get_nbest()

    def append_sentence_entity(self,se_pair):
        self.__sentence_entity.append(se_pair)
        
    #构建sentence entity
    def construct_sentence_entity(self):
        #先把所有answer取出来
        answers = self.get_answers()


        #对于每一个答案
        for answer in answers:

            #得到答案的内容
            content = answer.get_content()

            #sentence tokenize
            sentences = nlp.sent_tokenize(content)

            #对于每一个句子
            for sentence in sentences:

                finder = NgramEntityFinder(sentence)

                #找出所有实体
                entity = finder.extract_entity(display=False)

                #加入结果集中
                if len(entity) >0 :
                    self.append_sentence_entity((sentence,entity))

    def print_sentence_entity(self):
        for sentence,entity in self.__sentence_entity:
            print("%s\n%s\n%s"%(sentence,entity,100*"="))


    #抽象方法, title扩展类, 用于扩展实体, 每个类必须定义该方法
    #也就是算法的精华部分, 最后会输出扩展的实体
    @abstractmethod
    def expand(self):
        pass

    #主体调用的函数
    #先把句子中所有的实体都抽出来
    #再进行实体扩展, 然后进行评价
    def run(self):
        #抽取答案句子中的所有实体
        self.construct_sentence_entity()

        #扩展实体
        expand_terms = self.expand()

        #评价,这个还没有弄

    


    


