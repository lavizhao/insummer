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
from insummer.query_expansion.entity_expansioner import SynRelateExpansioner

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
    tratio,tquantity = 0,0
    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        ose = SynRelateExpansioner(q,finder,max_level=2,display=True)
        ratio,quantity = ose.run()
        tratio += ratio
        tquantity += quantity
        print(100*"=")

    print("平均命中率 : %s"%(tratio/qnum))
    print("平均命中个数 : %s"%(tquantity/qnum))

if __name__ == '__main__':
    print(__doc__)

    exp(500)

