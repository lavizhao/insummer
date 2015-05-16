#!/usr/bin/python3

'''
说明:这个文件的主要作用是给定一个句子(问题或者答案中的句子),能找到句子中所有的实体并返回
'''

#这是个实体发现的抽象方法,需求是给定一个句子(问句或者答案的句子),我们能够求出答案句子或问句中所有的实体,这个有一点像实体链接, 但是有一点不同的是(这个在entity util类里面有,我就不说了),e.g. How can i avoid getting sick in china? getting sick就要抽取出来,而这个在通常的KB里面都不是实体, 而且sick也是实体, 这个就算成get sick好了, 后期可能都要,可能要最大的可能要其他的
#应该包含的方法有
#__init__ 初始化
#find通用方法, 查找到所有的实体, 返回一个entity string 类的list, 这样做的好处是, 用entity string 进行封装, 使得里面的比如get sick这样的词组可以进行二次查询, 扩大搜索范围

from abc import ABCMeta, abstractmethod
from conceptnet5.language.english import normalize
from ..util import NLP
from ..knowledge_base import concept_tool

nlp = NLP()
cn_tool = concept_tool()
in_kb = cn_tool.kb_has_concept

class abstract_entity_finder(metaclass=ABCMeta):

    def __init__(self,sentence,words_filter=None):
        self.__sentence = sentence
        self.__words_filter = words_filter
        self.__entity = None

    #这个是抽象方法,是必须定义的
    #display 属性是debug用的, 可以打印几个阶段什么的
    #return 的是个entity string 的list
    @abstractmethod
    def find(self,display=False):
        pass

    def get_sentence(self):
        return self.__sentence

    #设定实体结果
    def set_entity(self,entity):
        assert len(entity) >= 0
        self.__entity = entity

    def get_entity(self):
        return self.__entity
        
    def filter_words(self):
        if self.__words_filter == None:
            return
        else:
            result = list(filter(self.__words_filter,self.__entity))
            return result

    def extract_entity(self,display=False):
        self.find(display)
        result = self.filter_words()
        if display:
            print("final  word:|| %s ||"%(result))
            print(100*"=")
        return result
        
class example_entity_finder(abstract_entity_finder):

    def __init__(self,question):
        abstract_entity_finder.__init__(self,question)

    def print(self):
        print(self.get_sentence().get_title())

    def find(self,display=False):
        print(display)


def stopwords_filter(word):
    if nlp.is_stopwords(word):
        return False
    else:
        return True
    
#这个类主要利用的方法是寻找出所有符合ngram的实体来, 当然现在我只考虑bigram
#注意这里的输入是每一句话,而不是一个答案
#那么我们的第一步是利用conceptNet内置的stem进行stem

class NgramEntityFinder(abstract_entity_finder):

    def __init__(self,sentence):
        abstract_entity_finder.__init__(self,sentence,stopwords_filter)

    def find(self,display=False):
        #第一步stem所有句子, 这里有将/替换成空格,这个比较有必要
        sent = self.get_sentence().replace('/',' ')
        sent = self.get_sentence().replace('-',' ')

        #先POS-tagging
        pos_sent = nlp.blob_tags(sent)

        #bigram
        bgm = nlp.bigrams(pos_sent)

        #cand 是已经确定候选的词的集合, 已经经过词形转换了,是个set
        cand = set([])
        for (word1,tag1),(word2,tag2) in bgm:
            
            sword1,sword2 = nlp.norm_text(word1),nlp.norm_text(word2)
            sword12 = sword1+"_"+sword2
            
            condition = self.build_condition(tag1,tag2)

            self.process_condition(sword1,sword2,sword12,cand,condition)

        if display==True:
            print("orign    sent:|| %s ||"%(self.get_sentence()))
            print("stem     sent:|| %s ||"%(stem_sent))
            print("tokenize sent:|| %s ||"%(tok_sent))
            print("pos-tag  word:|| %s ||"%(pos_sent))
            print("cand     word:|| %s ||"%(cand))

        self.set_entity(list(cand))
            
        return list(cand)
            
    #得到三种tag
    def get_small_tag(self,tag):
        if nlp.tag_is_noun(tag):
            return 'n'
        elif nlp.tag_is_verb(tag):
            return 'v'
        else:
            return 'o'
            
    #建状态可以输入的tag有以下几种,n->名词, v动词 , o其他
    def build_condition(self,tag1,tag2):
        t1,t2 = self.get_small_tag(tag1),self.get_small_tag(tag2)
        return t1+'+'+t2

    def add_both(self,word1,word2,word12,cand):
        if word12 not in cand and in_kb(word12) :
            cand.add(word12)
        else:
            if word1 not in cand and in_kb(word1) :
                cand.add(word1)
            if word2 not in cand and in_kb(word2) :
                cand.add(word2)

    def add_first(self,word1,cand):
        if word1 not in cand and in_kb(word1) :
            cand.add(word1)

    def add_last(self,word2,cand):
        if word2 not in cand and in_kb(word2) :
            cand.add(word2)
            
    def process_condition(self,word1,word2,word12,cand,condition):
        if condition == 'n+n' or condition == 'v+v':
            self.add_both(word1,word2,word12,cand)
        elif condition == 'n+v' or condition == 'v+n':
            self.add_both(word1,word2,word12,cand)
        elif condition == 'v+o' or condition == 'n+o':
            self.add_first(word1,cand)
        elif condition == 'o+v' or condition == 'o+n':
            self.add_last(word2,cand)

#这个类主要利用的方法是寻找出所有符合ngram的实体来, 当然现在我只考虑bigram
#注意这里的输入是每一句话,而不是一个答案
#那么我们的第一步是利用conceptNet内置的stem进行stem

class MoreNgramEntityFinder(abstract_entity_finder):

    def __init__(self,sentence):
        abstract_entity_finder.__init__(self,sentence,stopwords_filter)

    def find(self,display=False):
        #第一步stem所有句子, 这里有将/替换成空格,这个比较有必要
        sent = self.get_sentence().replace('/',' ')
        sent = self.get_sentence().replace('-',' ')

        #先POS-tagging
        pos_sent = nlp.blob_tags(sent)

        #bigram
        bgm = nlp.bigrams(pos_sent)

        #cand 是已经确定候选的词的集合, 已经经过词形转换了,是个set
        cand = set([])
        for (word1,tag1),(word2,tag2) in bgm:
            
            sword1,sword2 = nlp.norm_text(word1),nlp.norm_text(word2)
            sword12 = sword1+"_"+sword2
            
            condition = self.build_condition(tag1,tag2)

            self.process_condition(sword1,sword2,sword12,cand,condition)

        if display==True:
            print("orign    sent:|| %s ||"%(self.get_sentence()))
            print("stem     sent:|| %s ||"%(stem_sent))
            print("tokenize sent:|| %s ||"%(tok_sent))
            print("pos-tag  word:|| %s ||"%(pos_sent))
            print("cand     word:|| %s ||"%(cand))

        self.set_entity(list(cand))
            
        return list(cand)
            
    #得到三种tag
    def get_small_tag(self,tag):
        if nlp.tag_is_noun(tag):
            return 'n'
        elif nlp.tag_is_verb(tag):
            return 'v'
        else:
            return 'o'
            
    #建状态可以输入的tag有以下几种,n->名词, v动词 , o其他
    def build_condition(self,tag1,tag2):
        t1,t2 = self.get_small_tag(tag1),self.get_small_tag(tag2)
        return t1+'+'+t2

    def add_both(self,word1,word2,word12,cand):
        if word12 not in cand and in_kb(word12) :
            cand.add(word12)
        else:
            if word1 not in cand and in_kb(word1) :
                cand.add(word1)
            if word2 not in cand and in_kb(word2) :
                cand.add(word2)

    def add_first(self,word1,cand):
        if word1 not in cand and in_kb(word1) :
            cand.add(word1)

    def add_last(self,word2,cand):
        if word2 not in cand and in_kb(word2) :
            cand.add(word2)
            
    def process_condition(self,word1,word2,word12,cand,condition):
        if condition == 'n+n' or condition == 'v+v':
            self.add_both(word1,word2,word12,cand)
        elif condition == 'n+v' or condition == 'v+n':
            self.add_both(word1,word2,word12,cand)
        elif condition == 'v+o' or condition == 'n+o':
            self.add_first(word1,cand)
            self.add_first(word2,cand)
            self.add_first(word12,cand)
        elif condition == 'o+v' or condition == 'o+n':
            self.add_last(word2,cand)
            self.add_first(word1,cand)
            self.add_first(word12,cand)
            
