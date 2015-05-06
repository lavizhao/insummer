#!/usr/bin/python3

from data import get_duc

import sys
sys.path.append("..")
import insummer

from insummer.common_type import Question
from insummer.util import rule_based_sentence_cleaner as RBSC
from insummer.util import NLP

import random

def rand() :
    return random.random()

nlp = NLP()

rbsc = RBSC()

print("读数据")
questions = get_duc()

def main():

    cand_sent = []

    origin_length = 0
    new_length = 0
    
    for question in questions:
        for ans in question.get_nbest():
            content = ans.get_content()

            origin_length += nlp.sentence_length(content)
            
            sents = nlp.sent_tokenize(content)
            
            cand_sent.append(sents[0])

            for sent in sents:
                r = rand()
                if r < 0.2:
                    cand_sent.append(sent)

            ans.clean()
            new_length += nlp.sentence_length(ans.get_content())

    print("检测句子数量",len(cand_sent))
    print("原来单词数",origin_length)
    print("现在单词数",new_length)
    for sent in cand_sent:
        print("原句子|",sent)
        print("修正过|",rbsc.clean(sent))
        print(100*'=')

if __name__ == '__main__':
    main()
    


