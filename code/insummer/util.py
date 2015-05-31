'''
这个文件主要封装了一些常用的函数
'''

import nltk
from nltk import word_tokenize
from textblob import TextBlob
import textblob
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from textblob.tokenizers import SentenceTokenizer as sent_tok
from textblob.tokenizers import WordTokenizer as word_tok
from .read_conf import config

from .english import normalize


stopwords = open(config("../../conf/cn_data.conf")["stop_pos"])
stopwords = stopwords.readlines()
stopwords = [i.strip() for i in stopwords]


#定义所有NLP的方法
class NLP:
    def __init__(self):

        self.__np_extractor = textblob.en.np_extractors.ConllExtractor()

        self.__wnl = WordNetLemmatizer()

        self.__st = sent_tok()

        self.__wt = word_tok()

        self.__stopwords = set(stopwords)

    #用blob进行标注
    def blob_tags(self,sentence):
        blob = TextBlob(sentence)
        return blob.tags

    #用nltk进行标注
    def nltk_tags(self,sentence):
        tk = word_tokenize(sentence)
        return nltk.tag.pos_tag(tk)

    #将文本归一化,这个用的是conceptNet自带的归一化工具
    def norm_text(self,text):
        return normalize(text)

    #去html的tag
    def remove_tag(self,sentence):
        sentence = BeautifulSoup(sentence).get_text()
        sentence = sentence.split()
        sentence = ' '.join(sentence)
        return sentence

    #分句
    def sent_tokenize(self,sents):
        result = self.__st.tokenize(sents)
        return result

    def word_tokenize(self,sent):
        return self.__wt.tokenize(sent)
        

    def bigrams(self,sent_tok):
        return nltk.bigrams(sent_tok)
        
    def trigrams(self,sent_tok):
        return nltk.bigrams(sent_tok)

        
    #判断pos是不是名词,即以N或n开头
    def tag_is_noun(self,tag):
        if tag.startswith('N'):
            return True

        return False

    #判断pos是不是动词
    def tag_is_verb(self,tag):
        if tag.startswith('V'):
            return True

        return False

    def is_stopwords(self,word):
        return word in self.__stopwords

    def sentence_length(self,sent):
        words = self.word_tokenize(sent)
        count = 0
        for word in words:
            if len(word) >= 2:
                count += 1

        return count

    def sentence_length_exclude_stop(self,sent):
        words = self.word_tokenize(sent)
        count = 0
        for word in words:
            if len(word) >= 2 and self.is_stopwords(word)==False:
                count += 1

        return count

import re        
#句子过滤器
#这个主要是论文中压缩句子的方法
#Lu Wang. et al 2013 ACL中给出的七条规则
#rule1 : 去掉报头，（新闻语料特有），如[MOSCOW,October 19(XINHUA)] - 等
#rule2 : 去掉相对日期，如星期二
#rule3 : 去掉句子中间的一些插入语，如XXX, zhaoximo said,XXXX
#rule4 : 去掉领头的副词、形容词等，如Interesting， XXXX
#rule5 : 去掉名词的同位语（这个不好做）
#rule6 : 去掉一些由形容词或动名词等领导的从句，如Starting in 1990....
#rule7 : 去掉括号内的内容

from itertools import product

class rule_based_sentence_cleaner:
    def __init__(self):
        self.nlp = NLP()
        
    def clean_head(self,sent,head_symbol):
        if head_symbol in sent:
            sp = sent.split(head_symbol)
            sent = ' '.join(sp[1:])

        return sent


    def clean(self,sent):
        #先执行rule1 和rule7
        sent = sent.replace("``","")
        sent = sent.replace("\'\'","")

        if len(sent) < 5:
            sent = ""
            return sent


        #rule7 去掉括号内的内容
        regex = r"\(.+\)"
        replacement = " "

        sent = re.sub(regex,replacement,sent)
        
        #rule1 去掉-- 和 _ 之前的内容
        sent = self.clean_head(sent,"--")
        sent = self.clean_head(sent,"_")
        sent = self.clean_head(sent,":")
        
        sent = sent.strip()

        if len(sent) < 5:
            sent = ""
            return sent


        if sent[-1] != "." and sent[-1] != "?":
            sent += "."
        
        return sent

#传说中的内存存储
class mem_cache:
    def __init__(self,name):
        self.data = {}
        self.hit = 0
        self.total = 0
        self.name = name

    def add(self,key,value):
        self.data[key] = value

    def has(self,key,display = False):
        self.total += 1    
        if key in self.data:
            self.hit += 1
            if display:
                if self.hit % 100 == 0:
                    print("cache名",self.name,"命中率",self.hit/self.total,"总个数",self.total,"命中个数",self.hit)
            return self.data[key]

        return None

