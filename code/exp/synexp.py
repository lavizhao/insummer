#!/usr/bin/python3

__doc__ = '''
说明:
   功能: 单测basic-t1 和basic-t2和basic 下 duc 和yahoo answer的平均命中率和平均命中个数
   运行: ./synexp.py -d duc(ya) -l 1
         其中d表示数据集,l表示扩展层数
'''

#将模块insummer加入
import sys
sys.path.append("..")
import insummer

#将同义词扩展模块引入
from insummer.query_expansion.entity_expansioner import OnlySynExpansioner

#引入实体发现模块,暂定的是baseline的ngram模块
from insummer.query_expansion.entity_finder import NgramEntityFinder
finder = NgramEntityFinder

from optparse import OptionParser 

#引入数据模块
import data

import logging

#定义exp函数, 是实验的主体
#qnum是问题数据的个数
def exp(questions,qnum,l):
    tratio,tquantity,te = 0,0,0
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        ose = OnlySynExpansioner(q,finder,level=l,display=True)
        ratio,quantity,ee,dumb = ose.run()
        tratio += ratio
        tquantity += quantity
        te += ee
        print(100*"=")

    print("平均命中率 : %s"%(tratio/qnum))
    print("平均命中个数 : %s"%(tquantity/qnum))
    print("平均实体扩展个数: %s"%(te/qnum))

if __name__ == '__main__':
    print(__doc__)

    parser = OptionParser()  
    parser.add_option("-d", "--data", dest="data",help="选择数据集")
    parser.add_option("-l", "--level", dest="level",help="扩展层数")  
  
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

    level = int(options.level)

    length = len(questions)


    exp(questions,length,level)
    print("数据集 %s 数据长度 %s, 扩展层数 %s"%(options.data,length,level) )
    
    #exp(30)

