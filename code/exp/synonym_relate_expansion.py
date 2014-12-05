#!/usr/bin/python3

__doc__ = '''
说明:
   本实验的作用是测只用同义词扩展的效果, 命中了哪些实体等,将用data做实验,具体输出方法请看script下的数据脚本,数据请看相应的位置
'''

#将模块insummer加入
import sys
sys.path.append("..")
import insummer

#将同义词扩展模块引入
from insummer.query_expansion.entity_expansioner import SynRelateExpansioner,SynRankRelateExpansioner

#引入实体发现模块,暂定的是baseline的ngram模块
from insummer.query_expansion.entity_finder import NgramEntityFinder
finder = NgramEntityFinder

#引入数据模块
import data
print("载入数据...")
questions = data.get_data()


#定义exp函数, 是实验的主体
#qnum是问题数据的个数
def exp(qnum):
    tratio,tquantity,te = 0,0,0
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        ose = SynRankRelateExpansioner(q,finder,level1=1,level2=1,display=True)
        #ose = SynRelateExpansioner(q,finder,max_level=2,display=True)
        ratio,quantity,expand_entity = ose.run()

        #命中率
        tratio += ratio

        #命中个数
        tquantity += quantity

        #扩展实体个数
        te += expand_entity
        
        #ose.print_sentence_entity()
        print(100*"=")

    print("平均命中率 : %s"%(tratio/qnum))
    print("平均命中个数 : %s"%(tquantity/qnum))
    print("平均扩展实体个数: %s"%(te/qnum))

if __name__ == '__main__':
    print(__doc__)

    exp(100)

