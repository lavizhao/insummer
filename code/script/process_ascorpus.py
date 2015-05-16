#!/usr/bin/python3

'''
把as_corpus的摘要信息和答案、问题分开
'''

as_dir = "/home/lavi/project/insummer/as_corpus/all/"
as_data = "/home/lavi/project/insummer/as_corpus/as_data/"
as_sum = "/home/lavi/project/insummer/as_corpus/as_sum/"

import os

for fname in os.listdir(as_dir):
    dt = [] #问题和答案
    su = [] #摘要
    f = open(as_dir+fname)
    begin_su = False

    num = fname[:-4]
    
    for line in f:
        line = line.strip()
        if line.startswith("Abstract"):
            begin_su = True
            continue

        if begin_su == False:
            dt.append(line)
        else:
            su.append(line)

        file_dt = open(as_data+num+".questions","w")
        file_su = open(as_sum+num+".sum","w")

        for l in dt :
            file_dt.write(l+"\n")

        for l in su:
            file_su.write(l+"\n")    



