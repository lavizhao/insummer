#!/usr/bin/python3

'''
说明:这个文件的主要作用是给定一个句子(问题或者答案中的句子),能找到句子中所有的实体并返回
'''

#这是个实体发现的抽象方法,需求是给定一个句子(问句或者答案的句子),我们能够求出答案句子或问句中所有的实体,这个有一点像实体链接, 但是有一点不同的是(这个在entity util类里面有,我就不说了),e.g. How can i avoid getting sick in china? getting sick就要抽取出来,而这个在通常的KB里面都不是实体, 而且sick也是实体, 这个就算成get sick好了, 后期可能都要,可能要最大的可能要其他的
#应该包含的方法有
#__init__ 初始化
#find通用方法, 查找到所有的实体, 返回一个entity string 类的list, 这样做的好处是, 用entity string 进行封装, 使得里面的比如get sick这样的词组可以进行二次查询, 扩大搜索范围

from abc import ABCMeta, abstractmethod

class abstract_entity_finder(metaclass=ABCMeta):

    def __init__(self,question):
        self.question = question

    #这个是抽象方法,是必须定义的
    #display 属性是debug用的, 可以打印几个阶段什么的
    #return 的是个entity string 的list
    @abstractmethod
    def find(self,display=False):
        pass


class example_entity_finder(abstract_entity_finder):

    def __init__(self,question):
        abstract_entity_finder.__init__(self,question)

    def print(self):
        print(self.question.get_title())

    def find(self,display=False):
        print(display)

