#!/usr/bin/python3

__doc__ = '''
说明:
    功能: 测basic-t1(2)-r1(2) 下duc的平均命中率和命中个数
    运行: ./synrelate.py -d duc(ya) -t 1 -r 2
    其中d表示数据集,t和r分别表示同义层和关联层的层数
'''

#将模块insummer加入
import sys
sys.path.append("..")
import insummer

#将同义词扩展模块引入
from insummer.query_expansion.entity_expansioner import SynRelateExpansioner

#引入实体发现模块,暂定的是baseline的ngram模块
from insummer.query_expansion.entity_finder import NgramEntityFinder
finder = NgramEntityFinder

#引入数据模块
import data
import logging

from optparse import OptionParser 


#定义exp函数, 是实验的主体
#qnum是问题数据的个数
def exp(questions,qnum,l1,l2):
    tratio,tquantity,te,tf = 0,0,0,0
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        
        ose = SynRelateExpansioner(q,finder,level1=l1,level2=l2,display=True)
        ratio,quantity,expand_entity,filter_len = ose.run()

        #q.print()

        #命中率
        tratio += ratio

        #命中个数
        tquantity += quantity

        #扩展实体个数
        te += expand_entity

        #过滤实体个数
        tf +=  filter_len
        
        #ose.print_sentence_entity()
        print(100*"=")

    print("平均命中率 : %s"%(tratio/qnum))
    print("平均命中个数 : %s"%(tquantity/qnum))
    print("平均扩展实体个数: %s"%(te/qnum))
    print("平均同义层过滤后实体个数: %s"%(tf/qnum))

if __name__ == '__main__':
    print(__doc__)

    parser = OptionParser()  
    parser.add_option("-d", "--data", dest="data",help="选择数据集")
    parser.add_option("-t", "--level1", dest="level1",help="同义层层数")
    parser.add_option("-r", "--level2", dest="level2",help="同义层层数")
  
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


    length = len(questions)
    level1 = int(options.level1)
    level2 = int(options.level2)

    
    exp(questions,length,level1,level2)
    print("数据集%s 数据长度 %s, 同义层层数 %s 关联层层数 %s"%(options.data,length,level1,level2))
