#!/usr/bin/python3

'''
看看原始摘要的效果
'''

import sys
sys.path.append("..")
import insummer

import data
import logging
from optparse import OptionParser 

from insummer.summarization.ilp import traditional_ilp as TI

#定义exp函数, 是实验的主体
#qnum是问题数据的个数
def exp(questions,qnum):

    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        q.clean()
        ose = TI(q,250)

        result = ose.extract()

        print(result)
        ose.evaluation(result,'ilp')
        print(100*"=")

if __name__ == '__main__':
    print(__doc__)

    parser = OptionParser()  
    parser.add_option("-d", "--data", dest="data",help="选择数据集")

    (options, args) = parser.parse_args()
    
    print("载入数据")
    questions = ""
    if options.data == "ya":
        questions = data.get_data()
    elif options.data == "duc":
        questions = data.get_duc()
    else:
        logging.error("载入数据出现错误")
        sys.exit(1)
        
    exp(questions,len(questions))
        
