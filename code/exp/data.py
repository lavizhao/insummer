#!/usr/bin/python3
'''
这个文件主要测试载入数据
'''

import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config

import pickle

qconf = config("../../conf/question.conf")

data_dir = qconf["filter_qa"]

f = open(data_dir,'rb')

data = pickle.load(f)

def get_data():
    return data


if __name__ == '__main__':
    
    print("hello")
    
    print(len(data))
    data[0].print()
