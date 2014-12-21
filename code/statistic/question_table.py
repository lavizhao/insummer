#!/usr/bin/python3
#coding=utf-8

class question_table(object):
    def __init__(self,question_No,question_author):
        self.question_No = question_No
        self.question_author = question_author
        #question statistic
        self.qa_num = 0
        self.qw_num = 0
        self.qe_num = 0
        #title's
        self.te_num = 0
        self.tw_num = 0
        #answer's
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

    def update_question(self,qa,qw,qe):
        self.qa_num = qa
        self.qw_num = qw
        self.qe_num = qe
