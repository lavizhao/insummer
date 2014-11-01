#!/usr/bin/python3

'''
这个写出来是为了测试main包好不好使的
这个基本上是一个test的例子, 以后基本上就按照这个文件写
'''


import sys
sys.path.append("..")
import insummer
from insummer.query_expansion import EntityFinder
from insummer.read_conf import config

if __name__ == '__main__':
    conf = config("../../conf/question.conf")
    f = open(conf["title_pos"])
    titles = f.readlines()

    indx = 0
    for title in titles:
        if indx > 20:
            break

        naive_finder = EntityFinder(title)
        naive_finder.find(display=True)
        indx += 1
