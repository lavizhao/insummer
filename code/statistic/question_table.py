#!/usr/bin/python3
#coding=utf-8

class question_table(object):
    def __init__(self,question_No,question_author):
        self.question_No = question_No
        self.question_author = question_author
        
        #问题整体的答案数，单词数，实体数
        self.qa_num = 0
        self.qw_num = 0
        self.qe_num = 0

        #标题的实体数，单词数
        self.te_num = 0
        self.tw_num = 0

        #答案中所有答案的字典，整体的句子，实体，和单词数
        #具体单个回答的数目可以利用dict的中的值获得
        self.an_dict = {}
        self.an_sent = 0
        self.an_enti = 0
        self.an_word = 0

    def update_title(self,te,tw):
        self.te_num = te
        self.tw_num = tw

    def update_answer(self,idx,a_s,ae,aw):
        self.an_dict[idx] = tuple([a_s,ae,aw])
        self.an_sent += a_s
        self.an_enti += ae
        self.an_word += aw

    def update_question(self,qa_num):
        self.qa_num = qa_num

    def get_question(self):
        self.qw_num = self.tw_num + self.an_word
        self.qe_num = self.te_num + self.an_enti
        return self.qe_num,self.qw_num,self.qa_num
