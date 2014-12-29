#!/usr/bin/python3

#.py for test load data..

import sys
sys.path.append("../")
import insummer
from insummer.read_conf import config

import pickle

duc_conf = config('../../conf/question.conf')

def test_question(data_path):
    f = open(data_path,'rb')
    data = pickle.load(f)
    for idx in data:
        print(idx.get_count())
        print(idx.get_nbest())

if __name__ == "__main__":
    test_question(duc_conf['duc_question'])
