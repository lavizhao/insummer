
'''
说明：这个是最简单的摘要方法，主要用来进行测试抽取句子的效果
'''

from .summarizer import abstract_summarizer,ya_summarizer
from ..query_expansion.entity_expansioner import RankRelateFilterExpansioner as RFE
from ..query_expansion.entity_finder import NgramEntityFinder as ngram
from ..read_conf import config
from ..util import NLP

conf = config('/home/lavi/project/insummer/conf/question.conf')

nlp = NLP()

def sent_len(sent):
    words = nlp.word_tokenize(sent)
    count = 0
    for word in words:
        if len(word) >= 2:
            count += 1

    return count

class dummy1(abstract_summarizer):
    def __init__(self,q,word_limit):
        #先弄一个实体扩展类
        self.ep = RFE(q,ngram,1,1,display=False,n=40,length=100)

        self.question = q
        self.word_limit = word_limit

    def extract(self):

        print("返回实体权重")
        weighted_entity = self.ep.run()
        weighted_entity = dict(weighted_entity)

        print("返回所有句子+实体")
        entity_sent = self.ep.get_sentence_entity()

        #选出的句子
        result = {}

        #对于每个句子 加他的实体们
        for msent,ments in entity_sent:
            #初始得分为0 
            sent_score = 0

            for ment in ments:
                if ment in weighted_entity:
                    #简单加和
                    sent_score += weighted_entity[ment]

            if sent_score != 0:
                result[msent] = sent_score

        result = sorted(result.items(),key=lambda d:d[1],reverse=True)

        res = ""

        #现在句子的长度
        current_length = 0
        
        for sent,score in result:
            #得到句子的长度
            sent_length = sent_len(sent)
            if current_length >= self.word_limit:
                break
            else:
                if current_length + sent_length  <= self.word_limit:
                    res += sent
                    current_length += sent_length

        fuck_length = sent_len(res)
        print("句子总词数",fuck_length)
        
        wp = conf["dumm1_sum"]
        wp += self.question.get_author()
        wp = wp[:-1]

        f = open(wp,"w")
        f.write(res)
        f.close()
        
        return wp

import math

def transform_score(score):
    return math.log(score+1)
        
        
def transform_score1(score):
    result = 0        
    if score > 1000:
        result = 2 + result / 10000
    elif score > 100:
        result = 1 + result / 1000
    elif score > 10:
        result = 0.5 + result / 100
    else:
        result = 0.5

    return result
        
    
class dummy2(abstract_summarizer):
    def __init__(self,q,word_limit):

        #先弄一个实体扩展类
        self.ep = RFE(q,ngram,1,1,display=False,n=40,length=6000)

        self.question = q
        self.word_limit = word_limit

    def extract(self):

        print("问题标题",self.question.get_title())

        print("返回实体权重")
        weighted_entity = self.ep.run()
        weighted_entity = dict(weighted_entity)

        total_entity = set(weighted_entity.keys())
        
        for ent in weighted_entity:
            weighted_entity[ent] = transform_score(weighted_entity[ent])

        print("返回所有句子+实体")
        entity_sent = self.ep.get_sentence_entity()

        #选出的句子
        result = {}

        sent_with_entity = dict(entity_sent)

        #对于每个句子 加他的实体们
        for msent,ments in entity_sent:
            #初始得分为0 
            sent_score = 0

            for ment in ments:
                if ment in weighted_entity:
                    #简单加和
                    sent_score += weighted_entity[ment]

            if sent_score != 0:
                        
                sent_length = sent_len(msent)
                result[msent] = sent_score + math.log(sent_length)
                

        result = sorted(result.items(),key=lambda d:d[1],reverse=True)[:100]
        result = dict(result)        

        score_sum = sum(result.values())
        for sent in result:
            result[sent] /= score_sum

        result = sorted(result.items(),key=lambda d:d[1],reverse=True)[:100]
                
        res = ""

        #现在句子的长度
        current_length = 0
        entity_set = set()
        
        for sent,score in result:
            #得到句子的长度
            sent_length = sent_len(sent)
            if current_length >= self.word_limit:
                break
            else:
                if current_length + sent_length  <= self.word_limit:
                    print(sent,score)
                    print(set(sent_with_entity[sent]).intersection(total_entity))
                    print(150*"-")
                    res += sent
                    current_length += sent_length

        fuck_length = sent_len(res)
        print("句子总词数",fuck_length)
        
        wp = conf["dumm1_sum"]
        wp += self.question.get_author()
        wp = wp[:-1]

        f = open(wp,"w")
        f.write(res)
        f.close

        print(150 * "=")
        
        return wp
        
as_dir = "/home/lavi/project/insummer/as_corpus/all/"
as_data = "/home/lavi/project/insummer/as_corpus/as_data/"
as_sum = "/home/lavi/project/insummer/as_corpus/as_sum/"
as_res = "/home/lavi/project/insummer/as_corpus/as_res/"
as_best = "/home/lavi/project/insummer/as_corpus/all_best/"
class ya_dum(ya_summarizer):
    def __init__(self,Q,words,display=False):
        ya_summarizer.__init__(self,Q,words,display=display)

    def extract(self):
        #先得到名字
        wp = self.question.get_author()
        doc_num = wp.split("|")[0]

        best_name = as_best+doc_num + ".txt"
        total = open(best_name).readlines()
        total = ' '.join(total)

        fname = as_res+wp.split("|")[0]+".res"

        f = open(fname,"w")
        f.write(total)
        f.close()
        return fname
        
