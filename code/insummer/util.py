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
