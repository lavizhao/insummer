'''
这个文件主要封装了一些常用的函数
'''

import nltk
from nltk import word_tokenize
from textblob import TextBlob
import textblob
from nltk.tag.stanford import NERTagger
from nltk.tag.stanford import POSTagger
from nltk.stem import WordNetLemmatizer

#定义所有NLP的方法
class NLP:
    def __init__(self):
        self.__SNER = NERTagger('/home/lavi/package/stanford-ner1/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/lavi/package/stanford-ner1/stanford-ner.jar')
        self.__SPOS = POSTagger('/home/lavi/package/stanford-postagger/models/english-bidirectional-distsim.tagger','/home/lavi/package/stanford-postagger/stanford-postagger.jar')

        self.__np_extractor = textblob.en.np_extractors.ConllExtractor()

        self.__wnl = WordNetLemmatizer()


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
    def stanford_tags(self,sentence):
        tk = word_tokenize(sentence)
        return self.__SPOS.tag(tk)

    def lemma(self,word):
        return self.__wnl.lemmatize(word)
