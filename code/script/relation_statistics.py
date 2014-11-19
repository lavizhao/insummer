#!/usr/bin/python3

'''
这个文件的主要作用是统计relation的数据
'''
import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config
from insummer.knowledge_base import concept_tool
from insummer.knowledge_base.relation import relation_tool


#others
import csv

conf = config("../../conf/cn_data.conf")

data_pos = conf["csv_pos"]

part = [i for i in range(0,8)]

cp_tool = concept_tool()
rel_tool = relation_tool()

#得到第i份part的名字
def get_ipart_name(i):
    return "%spart_0%s.csv"%(data_pos,part[i])

def get_ipart_handler(i):
    assert int(i) in part
    
    fname = get_ipart_name(int(i))
    fi = open(fname)
    reader = csv.reader(fi,delimiter='\t')
    return reader

#三元组的限制
def triple_criterion(rel,cp1,cp2):
    if cp_tool.is_english_concept(cp1) and \
       cp_tool.is_english_concept(cp2) and \
       rel_tool.is_relation(rel):
        return True

    else:
        return False

def main():
    result = {}
    indx = 0

    #对于某个part来说,先打开,然后再挨个统计
    #line的1,2,3 分别是relation, cp1,cp2
    for ipart in part:
        #得到指针
        reader = get_ipart_handler(ipart)

        for line in reader:
            rel,cp1,cp2 = line[1],line[2],line[3]
            #如果满足限制条件
            if triple_criterion(rel,cp1,cp2):
                #print("%30s%30s%30s"%(rel,cp1,cp2))
                #下面处理是neg还是pos
                positive = 'pos' if rel_tool.is_pos(rel) else 'neg'
                rel_name = rel_tool.rel_name(rel)
                result.setdefault(rel_name,{})
                result[rel_name].setdefault('pos',0)
                result[rel_name].setdefault('neg',0)

                result[rel_name][positive] += 1
                indx += 1
                if indx %10000 == 0:
                    print(indx)

    #循环完了,该输出统计了
    for rel_name in result:
        sta = result[rel_name]
        print("relation name : %30s , pos : %20s , neg : %20s"%(rel_name,sta['pos'],sta['neg']))
    
#这个就不用其他功能了, 省得弄得非常蛋疼    
if __name__ == '__main__':
    main()
    
