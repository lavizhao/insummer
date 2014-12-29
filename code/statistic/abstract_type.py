#!/usr/bin/python3
#coding=utf-8

class abstract_type(object):
    def __init__(self,title,answer):
        self.title = title
        self.answer = answer
        self.abstract = ''

    def update_abstract(self,abstract):
        self.abstract = abstract
