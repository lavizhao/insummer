#!/usr/bin/python3

'''
说明:这个文件是查询扩展类,主要负责查询扩展方面的工作
'''

import sys
from abc import ABCMeta, abstractmethod
from ..common_type import Question
from ..util import NLP
from .entity_finder import NgramEntityFinder
from ..knowledge_base.entity_lookup import ConceptnetEntityLookup
from ..evaluation import bias_overlap_ratio

nlp = NLP()
searcher = ConceptnetEntityLookup()

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

        #这个是所有句子中所有的实体
        self.__sentence_total_entity = set([])

        self.__expand_entity = None

    def get_title(self):
        return self.__question.get_title()
        
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

                #把总实体相加
                self.__sentence_total_entity = self.__sentence_total_entity.union(set(entity))

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

        
    #评价实体扩充的好坏, 这个方法因为不唯一, 所以也有可能扩充到好几个方法
    #expand terms是一个set
    #另一个现有的数据是self.__sentence_entity, 因为可以直接访问到, 所以不会另建一个
    def evaluation(self,expand_terms):
        #print(self.__sentence_total_entity)
        return bias_overlap_ratio(expand_terms,self.__sentence_total_entity)
        
    #主体调用的函数
    #先把句子中所有的实体都抽出来
    #再进行实体扩展, 然后进行评价
    def run(self):
        #抽取答案句子中的所有实体
        self.construct_sentence_entity()

        #扩展实体
        expand_terms = self.expand()

        #评价,这个还没有弄
        result = self.evaluation(expand_terms)

        print("====",result)
    
#这个算法只扩展同义词类
class OnlySynExpansioner(abstract_entity_expansioner):
    #max level是可扩展到最大层数, 如需要两层 则level = 2
    def __init__(self,mquestion,entity_finder,max_level):
        abstract_entity_expansioner.__init__(self,mquestion,entity_finder)
        self.level = max_level

    #扩展
    def expand(self):
        title = self.get_title()

        base_entity = set()

        #先抽取问题的实体
        sentences = nlp.sent_tokenize(title)
        for sentence in sentences:
            print(sentence)
            finder = NgramEntityFinder(sentence)
            entity = finder.extract_entity()
            if len(entity) > 0:
                base_entity = base_entity.union(set(entity))

        #开始扩展
        #算法流程打算用基于栈的非递归方法
        
        #1. 记录当前的实体数量
        previous_entity_length = len(base_entity)
        #print(base_entity)

        #2. expand_entity初始化设为base_entity
        expand_entity = base_entity.copy()

        #3. 假设扩展之前 a,b,c 当a,b,c 都扩展完之后, 需要与之前的比较大小, 那么之前的需要初始化进行记录
        previous_expand_entity = expand_entity.copy()

        #4. 判断条件, 1. expand_entity 的体积没有增长, 2.previous_expand_entity 已经遍历完了
        indx = 0
        while indx < self.level:

            #对每个前一轮的实体来说
            for entity in previous_expand_entity:
                #进行同义词扩展
                temp_expand_entity = searcher.synonym_entity(entity)

                #合并
                expand_entity = expand_entity.union(temp_expand_entity)
                
            #print("level %s , length %s : %s "%(indx,len(expand_entity),expand_entity))
            indx += 1    
            #扩展的集合体积没有增长, 则说明循环结束, 跳出循环, 如不然则重新赋值
            if len(expand_entity) == previous_expand_entity:
                break;
            else:
                previous_entity_length = len(expand_entity)
                previous_expand_entity = expand_entity.copy()

        return expand_entity


