#!/usr/bin/python3

'''
创建insunnet, 用mangodb进行存储
'''

import csv
import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config
from insummer.knowledge_base import concept_tool
from insummer.knowledge_base.relation import relation_tool

import pymongo

#创建数据库直接用的mongodbimport, 所以在这里没有体现


class db_handler():
    def __init__(self):
        self.__usr = 'root'
        self.__pwd = ''
        conn = pymongo.Connection('localhost',27017)
        self.__db = conn.insunnet
        self.tbl = self.__db.assertion

    #建索引, 这个直接写死在里面了
    def single_indx(self,entity):
        print("create indx on %s"%(entity))
        self.tbl.create_index([(entity,1)])

    def double_indx(self,entity,rel):
        print("create indx on %s %s"%(entity,rel))
        self.tbl.create_index([(entity,1),(rel,1)])

    def create_indx(self):
        print("建索引")    
        entity = ["start","end"]
        rel = "rel"

        for ent in entity:
            self.single_indx(ent)
            self.double_indx(ent,rel)
        

if __name__ == '__main__':
    mong = db_handler()
    mong.create_indx()
