'''
说明:这里放着的就只是一个摘要的抽象类, 给看接口用的
'''

from abc import ABCMeta, abstractmethod

#Q是question类
#words是最长字数
#display是显示信息
class abstract_summarizer(metaclass=ABCMeta):
    def __init__(self,Q,words,display=False):
        self.__question = Q
        self.display = display
        self.words_limit = words

    def get_question(self):
        return self.__question

    def get_words_limit(self):
        return self.words_limit

    #抽象方法
    #返回一个sentence的list, sentence的词数之和小于word_limit.
    #现在先这么写着,到时候再换
    @abstractmethod
    def extract(self):
        pass

    #评价, 用rouge进行评价
    @abstractmethod
    def eveluation(self,result):
        pass

    #总的接口, 外面的主要调用这个跑
    def run(self):
        #先抽
        result = self.extract()

        #计算rouge
        rouge = self.eveluation(result)

        #如果display
        if display :
            print("rouge %s"%(rouge))
