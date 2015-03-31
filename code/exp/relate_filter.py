#!/usr/bin/python3

__doc__ = '''
说明:
    功能：测试pagerank,hits,cc,kcore等方法在duc和yahoo answer下参数
    运行：./
'''

#将模块insummer加入
import sys
sys.path.append("..")
import insummer

#将同义词扩展模块引入
from insummer.query_expansion.entity_expansioner import RankRelateFilterExpansioner

#引入实体发现模块,暂定的是baseline的ngram模块
from insummer.query_expansion.entity_finder import NgramEntityFinder
finder = NgramEntityFinder

#引入数据模块
import data
import logging
from optparse import OptionParser 

#定义exp函数, 是实验的主体
#qnum是问题数据的个数
def exp(questions,qnum,tmaxl,rmaxl):
    tratio,tquantity,te,tf = 0,0,0,0
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        ose = RankRelateFilterExpansioner(q,finder,1,1,display=True,n=tmaxl,length=rmaxl)
        ratio,quantity,expand_entity,filter_len = ose.run()

        #命中率
        tratio += ratio

        #命中个数
        tquantity += quantity

        #扩展实体个数
        te += expand_entity

        #过滤实体个数
        tf +=  filter_len
        
        #ose.print_sentence_entity()
        print(150*"=")

    print("平均命中率 : %s"%(tratio/qnum))
    print("平均命中个数 : %s"%(tquantity/qnum))
    print("平均扩展实体个数: %s"%(te/qnum))
    print("平均同义层过滤后实体个数: %s"%(tf/qnum))

if __name__ == '__main__':
    print(__doc__)

    parser = OptionParser()  
    parser.add_option("-d", "--data", dest="data",help="选择数据集")
    parser.add_option("-t","--tmaxl",dest="tmaxl",help="同义层最大个数")
    parser.add_option("-r","--rmaxl",dest="rmaxl",help="关联层最大个数")
    

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
    tmaxl = int(options.tmaxl)
    rmaxl = int(options.rmaxl)
        
    exp(questions,length,tmaxl,rmaxl)
        
    print("数据集%s，数据长度%s，同义层最大个数%s,关联层最大个数%s"%(options.data,length,tmaxl,rmaxl))    
