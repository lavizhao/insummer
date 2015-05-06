'''
这个文件主要封装了一些常用的函数
'''

import nltk
from nltk import word_tokenize
#from nltk.corpus import stopwords
from textblob import TextBlob
import textblob
#from nltk.tag.stanford import NERTagger
#from nltk.tag.stanford import POSTagger
from nltk.stem import WordNetLemmatizer
from conceptnet5 import nodes
from bs4 import BeautifulSoup
from textblob.tokenizers import SentenceTokenizer as sent_tok
from textblob.tokenizers import WordTokenizer as word_tok
from conceptnet5.language.english import normalize
ncc = nodes.normalized_concept_name
from .read_conf import config

stopwords = open(config("../../conf/cn_data.conf")["stop_pos"])
stopwords = stopwords.readlines()
stopwords = [i.strip() for i in stopwords]


#定义所有NLP的方法
class NLP:
    def __init__(self):
        #self.__SNER = NERTagger('/home/lavi/package/stanford-ner1/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/lavi/package/stanford-ner1/stanford-ner.jar')
        #self.__SPOS = POSTagger('/home/lavi/package/stanford-postagger/models/english-bidirectional-distsim.tagger','/home/lavi/package/stanford-postagger/stanford-postagger.jar')

        self.__np_extractor = textblob.en.np_extractors.ConllExtractor()

        self.__wnl = WordNetLemmatizer()

        self.__st = sent_tok()

        self.__wt = word_tok()

        #self.__stopwords = set(stopwords.words('english'))
        self.__stopwords = set(stopwords)

    #用blob进行标注
    def blob_tags(self,sentence):
        blob = TextBlob(sentence)
        return blob.tags

    #用blob进行名词短语抽取
    def blob_np(self,sentence):
        return self.__np_extractor.extract(sentence)

    #用nltk进行标注
    def nltk_tags(self,sentence):
        tk = word_tokenize(sentence)
        return nltk.tag.pos_tag(tk)

    #用stanford进行标注
    #def stanford_tags(self,sentence):
    #    tk = word_tokenize(sentence)
    #    return self.__SPOS.tag(tk)

    #将文本归一化,这个用的是conceptNet自带的归一化工具
    def norm_text(self,text):
        #return ncc('en',word)
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
class rule_based_sentence_cleaner:
    def __init__(self):
        self.nlp = NLP()

    def clean_head(self,sent,head_symbol):
        if head_symbol in sent:
            sp = sent.split(head_symbol)
            sent = ' '.join(sp[1:])

        return sent

    #去掉插入语,如XXX said
    def clean_intra_sent(self,sent):
        cand = ["said","saying","says","say"]

        anyone = False
        for s in cand:
            if s in sent:
                anyone = True

        if anyone == False:
            return sent

        #===============================
            
        sp = sent.split(',')
        ans = []

        for one in sp:
            one = one.strip()
            if one[-1] == "." or one[-1] == "?":
                one = one[:-1]

            dt = False
            for s in cand:
                if one.endswith(s) and len(one.split()) <= 5:
                    dt = True
                if one.startswith(s) and len(one.split()) <= 5:
                    dt = True    
                    
            if dt == False:
                ans.append(one)

            
        res =  ' , '.join(ans)

        if len(res.strip()) == 0:
            return " "
                
        if res[-1] != '.' and res[-1] != '?':
            res += "."
        return res
        
        
    def clean(self,sent):
        #先执行rule1 和rule7
        sent = sent.replace("``","")
        sent = sent.replace("\'\'","")
        
        #rule7 去掉括号内的内容
        regex = r"\(.+\)"
        replacement = " "

        sent = re.sub(regex,replacement,sent)
        
        #rule1 去掉-- 和 _ 之前的内容
        sent = self.clean_head(sent,"--")
        sent = self.clean_head(sent,"_")

        sent = self.clean_intra_sent(sent)

        return sent

        
        
    
