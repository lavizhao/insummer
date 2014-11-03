#!/usr/bin/python3

'''
这个文件主要专注于查询扩展方面的工作

'''
from .util import *
from .read_conf import config
from .common_type import Question

nlp = NLP()

#查询扩展的类
#初始化需要传入一个question的类
class QueryExpansion:
    def __init__(self,question):
        self.__question = question
        
#实体发现类,发现句子中的实体
class EntityFinder:
    def __init__(self,sentence):
        self.__sentence = sentence

    #找到所有的实体方法,这个是对外的接口
    #可以调为输出模式,打印所有三个步骤的输出,默认不输出    
    def find(self,display=False):
        #得到所有的名词短语
        noun_phrase = self.__extract_np()

        #进行stem,得到扩展后的实体
        extend_noun_phrase = self.__stem()

        #进行约减,得到最终的实体候选
        final_entity = self.__rule_reduction()

        if display==True:
            print("原来的句子====>%s"%(self.__sentence))
            print("所有np为===>%s"%(noun_phrase))
            #print("stem后扩展的np为====>%s"%(extend_noun_phrase))
            #print("最后得到的实体为====>%s"%(final_entity))
            print(20*"=")

        return final_entity

    
    #抽取出句子的所有名词短语(noun phrase)===>返回一个list
    def __extract_np(self):

        #先得到标注结果
        tag_result = nlp.blob_tags(self.__sentence)

        print("tag结果===>%s"%(tag_result))

        #得到名词短语结果
        np_result = nlp.blob_np(self.__sentence)

        #对tag进行循环,找出不在np_result中的名词
        noun_result = []

        #记个索引
        indx = 0
        #循环
        for (word,tag) in tag_result:
            #弄个变量记一下
            add_bool = False
            #准备添加的词
            add_word = ""

            if tag=='NN' or tag=='NNS' or tag == 'NNP':
                add_bool = True
                #检查是不是名词短语的一个子串
                if len(np_result) != 0:
                    for np in np_result:
                        if word in np:
                            add_bool = False

                #额外添加一下,如果单词是NNS的话,那么把后缀去了
                word = nlp.lemma(word)
                add_word = word
                        
            #抽取动词短语,如getting sick, look bigger等
            elif tag in set(['VB','VBG','VBN','VBP','VBZ']) :
                #判断一下,有没有越界
                if indx != (len(tag_result)-1):
                    word1,tag1 = tag_result[indx+1]
                    if tag1 in set(['JJ','JJR','VBN','RB','RBR']):
                        add_bool = True
                        
                        word = nlp.lemma(word)
                        word1 = nlp.lemma(word1)
                        add_word = word + " "+word1
                        
            else:
                add_bool = False

            if add_bool == True:
                noun_result.append(add_word)


            indx += 1
        #end for
        #再次词干还原一下    
        np_another = np_result[:]
        np_result = []
        for word in np_another:
            split_word = word.split()
            split_word = [nlp.lemma(i) for i in split_word]
            np_result.append(' '.join(split_word))
        np_result.extend(noun_result)
        
        return np_result

    #给所有候选实体stem,得到一个更广义的实体集
    def __stem(self):
        return []

    #利用规则的方法对候选实体进行约减,确定最终的实体集合
    def __rule_reduction(self):
        return []
        
#只用title建立一个比较粗浅的question类
def build_naive_question(title):
    return Question(title,"","",[])
    
#第一步做一下实验,看看nltk,textblob和其他我能想到的效果都怎么样
def test():
    conf = config("../../conf/question.conf")
    f = open(conf["title_pos"])
    titles = f.readlines()

    indx = 0
    for title in titles:
        if indx > 20:
            break

        #开始搞了
        print(title)
        print("nltk==>",nlp.nltk_tags(title))
        print("blob==>",nlp.blob_tags(title))
        print("np====>",nlp.blob_np(title))
        print(20*"=")
        indx += 1

def test2():
    conf = config("../../conf/question.conf")
    f = open(conf["title_pos"])
    titles = f.readlines()

    indx = 0
    for title in titles:
        if indx > 20:
            break

        naive_finder = EntityFinder(title)
        naive_finder.find(display=True)
        indx += 1
        
if __name__ == '__main__':
    test2()


