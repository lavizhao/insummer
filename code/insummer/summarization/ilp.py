
'''
这个文件的主要作用是记录所有ILP的方法， 如果记不下就另来一个文件
'''

from .summarizer import abstract_summarizer
from ..query_expansion.entity_expansioner import RankRelateFilterExpansioner as RFE
from ..query_expansion.entity_finder import NgramEntityFinder as ngram
from ..read_conf import config
from ..util import NLP

from pulp import *
import sys

nlp = NLP()

import math

conf = config('/home/lavi/project/insummer/conf/question.conf')

def sent_len(sent):
    words = nlp.word_tokenize(sent)
    count = 0
    for word in words:
        if len(word) >= 2:
            count += 1

    return count


#这个方法叫tranditional_ilp好了，就是经典没有任何改动的ILP方法
#ep         , 实体扩展类
#q          , 问题
#word_limit , 字数限制，一般是250
#answer_total_entities                 , 答案中全部的实体
#answer_entities_list                  , 答案中句子和实体组成的list[(e1,w1),(e2,w2)...]
#hit_entities                          , 命中实体的权重
#hit_entities_freq                     , 命中实体的频率
#unhit_entities                        , 未命中实体，权重全部为-1

#candidate_sentence_entities_dict      , 候选答案句子和实体组成的dict[(e1:w1),(e2:w2)....]
#sent_index                            , 候选答案句子的索引
#sent_inverse_index                    , 候选答案句子的逆索引
#sent_length                           , 候选答案句子的长度
#entity_index                          , 候选实体的索引
#entity_inverse_index                  , 候选实体的逆索引

#OCC                                   , 构建出现矩阵OCC[i][j] 为实体I在句子J中出现了没
class traditional_ilp(abstract_summarizer):
    def __init__(self,q,word_limit=250):
        self.ep = RFE(q,ngram,1,1,display=False,n=100,length=12000)
        self.question = q
        self.word_limit = word_limit
        print("文章题目",self.question.get_title())


    def extract(self):
        #执行生成摘要前的预备工作
        print("进行生成摘要前的准备工作")
        self.init_step()

        print("命中实体数目",len(self.hit_entities_freq),len(self.hit_entities)) 
        print("答案实体总数",len(self.answer_total_entities))

        print("进行整数规划前的准备工作")
        self.ilp_prepare()

        print("过滤前句子大小",len(self.answer_entities_list))
        print("过滤后句子大小",len(self.candidate_sentence_entities_dict))
        print("句子索引大小",len(self.sent_inverse_index),len(self.sent_index))
        print("实体索引大小",len(self.entity_inverse_index),len(self.entity_index))

        result = self.ilp()
        
        return result 

        
    #执行生成摘要前的输入工作
    #主要是得到命中实体和没有命中的实体
    #还有命中实体的频率，（未命中的就没必要了）
    #还有对实体的打分进行转换
    def init_step(self):
        ##先进行实体扩展，得到的实体是具有权重的list，[(e1,w1),(e2,w2)]
        expand_entities = self.ep.run()
        ##需要转化成字典形式，方便计算
        dict_expand_entities = dict(expand_entities)

        ##得到答案中的所有实体,加个set
        answer_total_entities = set(self.ep.get_sentence_total_entity())
        self.answer_total_entities = answer_total_entities


        #记录实体，这里实体总共有两部分，一部分命中的，一部分没有，分别叫hit和unhit好了
        #这里容易产生歧义的是，unhit不是指扩展实体中没有命中的部分，指的是答案实体中没有命中的部分    
        self.hit_entities      = {}
        self.unhit_entities    = {}

        #记录命中实体的频率
        self.hit_entities_freq = {}

        #====> 找到命中实体
        #对于所有这些扩展的实体
        for mentity in dict_expand_entities:
            #如果实体在 答案所有的实体里
            if mentity in answer_total_entities:
                mscore = dict_expand_entities[mentity]

                #将其加入到hit_entities中
                self.hit_entities[mentity] = mscore

            #如果不在，直接撇了
            #pass

        

            
        #====> 找到没有命中的实体
            
        #返回所有句子和实体的列表
        answer_entities_list = self.ep.get_sentence_entity()
        self.answer_entities_list = answer_entities_list
        
        #没有命中的实体主要是得遍历句子中的所有实体
        for manswer_sent,mentities in answer_entities_list:
            #遍历mentities,找到没有命中的实体
            for mentity in mentities:
                if mentity not in self.hit_entities:
                    self.unhit_entities[mentity] = -1.0

                #对于是hit_entities的实体
                else:
                    self.hit_entities_freq.setdefault(mentity,0)
                    self.hit_entities_freq[mentity] += 1

        #===========================================================================
        #=====> 在这里定义一个子函数，方便进行分数转换
        def transform_score(score,entity):
            return math.log(score+1) + self.hit_entities_freq[entity] * 5
                    
        #对所有的命中实体进行分数的转换
        for mentity in self.hit_entities:
            mscore = self.hit_entities[mentity]
            self.hit_entities[mentity] = transform_score(mscore,mentity)


                    
                    
    #整数规划的输入阶段
    #在这个阶段准备整数规划所需要的数据
    #主要包括: 1得到候选句子集合（过滤掉无关的句子）；2得到扩展实体的子集；3对实体和候选句子进行标号；4.构建句子和实体的OCC矩阵；
    def ilp_prepare(self):

        self.candidate_sentence_entities_dict = {}
        #给标号初始化
        self.sent_index           = {}
        self.sent_inverse_index   = {}
        self.sent_length          = {}
        self.entity_index         = {}
        self.entity_inverse_index = {}

        #两个索引现存的标号
        entity_index_number = 0
        sent_index_number = 0

        #====> step1：得到候选句子集合 , 句子标号的工作可能现在直接就做了

        hit_entities_set = set(self.hit_entities.keys())

        count = 0
        #对于答案的每个句子来说
        for manswer_sent,mentities in self.answer_entities_list:
            #先做个集合出来
            mentities_set = set(mentities)
            a1 = mentities_set

            #对于句子，进行strip，去两端
            manswer_sent  = manswer_sent.strip()

            #所有实体和临时集合取交集
            intersec_num  = len(mentities_set.intersection(hit_entities_set))
            mentities_set = mentities_set.intersection(hit_entities_set)
            a2 = mentities_set

            #如果没有交集，那么直接扔了
            if intersec_num <= 5 or sent_len(manswer_sent) < 5 :
                pass
            else:
                #先进行判断，句子在不在句子索引中
                #如果在，什么都不做
                if manswer_sent in self.sent_index:
                    pass
                else:
                    #添加答案句子索引
                    self.sent_index[manswer_sent] = sent_index_number
                    self.sent_inverse_index[sent_index_number] = manswer_sent
                    sent_index_number += 1
                    
                    self.candidate_sentence_entities_dict[manswer_sent] = mentities_set
                
        #====> step2：得到扩展实体子集
        #扩展实体的子集就是 hit_entities , 所以这个集合求过了        

    
        #====> step3：给实体标号
        for mentity in self.hit_entities:
            self.entity_index[mentity] = entity_index_number
            self.entity_inverse_index[entity_index_number] = mentity
            entity_index_number += 1

        
            
        #====> step4：构建OCC矩阵
        self.OCC = [[0 for j in range(len(self.sent_index))]  for i in range(len(self.entity_index))]
        print("OCC矩阵shape",len(self.OCC),len(self.OCC[0]))

        #对于每个 candidate_sentence_entities_dict 中的句子和实体， 下面填充OCC矩阵的工作
        for manswer_sent in self.candidate_sentence_entities_dict:
            #找到其实体集
            mentities_set = self.candidate_sentence_entities_dict[manswer_sent]

            #得到句子的索引
            msent_index = self.sent_index[manswer_sent]

            #对于每个实体来说
            for mentity in mentities_set:
                #找到这个实体的索引
                mentity_index = self.entity_index[mentity]

                #现在实体  (i=menetity_index )  ,  (j=msent_index)
                self.OCC[mentity_index][msent_index] = 1

        print("OCC矩阵构建完成")

    def ilp(self):
        print("ILP开始")    
        #====> 定义问题
        prob = LpProblem("ILP for summarization problem",LpMaximize)

        #变量的字典
        x_var = []
        y_var = []

        for indx in self.entity_inverse_index:
            x_var.append("x%s"%(indx))

        for indx in self.sent_inverse_index:
            y_var.append("y%s"%(indx))

        print("建立variable,类别全部设为binary")
        #====> 建立variable,类别全部设为binary
        x_lpvariable = LpVariable.dicts("entity",x_var,cat=LpInteger,lowBound=0,upBound=10)
        y_lpvariable = LpVariable.dicts("sent",  y_var,cat=LpInteger,lowBound=0,upBound=1)

        #获取ILP变量的权重
        def variable_weight(var):
            #首字母和尾字母
            first,last = var[0],var[1:]
            if first == "y":
                #得到句子名字
                variable_name = self.sent_inverse_index[int(last)]

                #得到句子长度
                sl = sent_len(variable_name)

                #得到句子实体数目
                el = len(self.candidate_sentence_entities_dict[variable_name])

                #return (sl) * 4 
                return 0 
            elif first == "x":
                #得到变量实体的名字
                variable_name = self.entity_inverse_index[int(last)]
                
                #得到相应的权重
                w = self.hit_entities[variable_name]
                
                return w

            else :
                print("获取权重信息有误")
                sys.exit(1)
                

        print("设立优化目标")
        obj1 = [x_lpvariable[i] * variable_weight(i) for i in x_var ]
        obj2 = [y_lpvariable[i] * variable_weight(i) for i in y_var ]
        obj1.extend(obj2)
        tobj = obj1
        prob += lpSum( tobj )

        #定义一个求句子长度的函数
        def variable_length(var):
            first,last = var[0],var[1:]
            if first == "y":
                #得到句子
                msent = self.sent_inverse_index[int(last)]
                #得到句子长度
                ml = sent_len(msent)
                return ml
            else:
                print("变量有问题")
                sys.exit(1)

        print("句子长度限制")
        #满足长度限制
        prob += lpSum([y_lpvariable[i] * variable_length(i) for i in y_var]) <= self.word_limit


        print("出现次数限制")
        #满足出现次数限制
        #对每个实体而言
        for i in range(len(self.entity_index)):
            nobj = []
            
            #对每个句子都有
            for j in range(len(self.sent_index)):
                nobj.append(self.OCC[i][j] * y_lpvariable["y%s"%(j)])

            nobj.append(-1 * x_lpvariable["x%s"%(i)])
                
            prob += lpSum( nobj ) == 0



        print("开始求解")
        prob.solve()
        print("Status:", LpStatus[prob.status])
        
        sent_list = []
        for v in prob.variables():
            sp = v.name.split('_')
            if sp[0] == "sent" and v.varValue > 0 :
                indx = int(sp[1][1:])
                msent = self.sent_inverse_index[indx]
                sent_list.append(msent)
            else:
                pass


        sent_length = 0
        for msent in sent_list:
            print(msent,self.candidate_sentence_entities_dict[msent])
            sent_length += sent_len(msent)

        print("摘要长度",sent_length)
            
        print("Total Cost of Ingredients per can = ", value(prob.objective))

        print("ILP结束")

        print("写入文件")
        wp = conf["ilp_sum"]
        wp += self.question.get_author()
        wp = wp[:-1]

        f = open(wp,"w")
        for msent in sent_list:
            f.write(msent+" ")

        f.close()
        return wp    
