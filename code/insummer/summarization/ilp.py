
'''
这个文件的主要作用是记录所有ILP的方法， 如果记不下就另来一个文件
'''

from .summarizer import abstract_summarizer
from ..query_expansion.entity_expansioner import RankRelateFilterExpansioner as RFE
from ..query_expansion.entity_finder import NgramEntityFinder as ngram
from ..query_expansion.entity_finder import MoreNgramEntityFinder as mngram
from ..read_conf import config
from ..util import NLP

from pulp import *
import sys

nlp = NLP()

import math

conf = config('/home/lavi/project/insummer/conf/question.conf')

#abstract_ilp
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
class abstract_ilp(abstract_summarizer):
    def __init__(self,q,word_limit,entity_finder,alpha,beta,unseen_limit,min_el,min_sl,max_sl):
        abstract_summarizer.__init__(self,q,word_limit)
        self.question = q
        self.alpha = alpha
        self.beta = beta
        self.unseen_limit = unseen_limit
        self.min_el = min_el
        self.min_sl = min_sl
        self.max_sl = max_sl
        self.word_limit = word_limit

    def extract(self):
        #执行生成摘要前的预备工作
        self.init_step(self.alpha,self.beta,self.unseen_limit)

        self.ilp_prepare(self.min_el,self.min_sl,self.max_sl)

        result = self.ilp()
        
        return result

        
    #执行生成摘要前的输入工作
    #主要是得到命中实体和没有命中的实体
    #还有命中实体的频率，（未命中的就没必要了）
    #还有对实体的打分进行转换
    def init_step(self,alpha,beta,unseen_limit):
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
        self.unhit_entities_freq = {}

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
                    
                    self.unhit_entities_freq.setdefault(mentity,0)
                    self.unhit_entities_freq[mentity] += 1

                #对于是hit_entities的实体
                else:
                    self.hit_entities_freq.setdefault(mentity,0)
                    self.hit_entities_freq[mentity] += 1

        #===========================================================================
        #=====> 在这里定义一个子函数，方便进行分数转换

        def transform_score(score,entity):
            freq = self.hit_entities_freq[entity]
            wt = math.log(score + beta) + alpha *  math.log( freq / len(self.answer_entities_list) )
            return wt

                    
        #对所有的命中实体进行分数的转换
        for mentity in self.hit_entities:
            mscore = self.hit_entities[mentity]
            self.hit_entities[mentity] = transform_score(mscore,mentity)

        for mentity in self.unhit_entities:
            freq = self.unhit_entities_freq[mentity]
            if freq >= self.unseen_limit:
                mscore = math.log(freq + beta) + alpha *  math.log(freq / len(self.answer_entities_list))
                self.hit_entities[mentity] = mscore
                    
    #整数规划的输入阶段
    #在这个阶段准备整数规划所需要的数据
    #主要包括: 1得到候选句子集合（过滤掉无关的句子）；2得到扩展实体的子集；3对实体和候选句子进行标号；4.构建句子和实体的OCC矩阵；
    def ilp_prepare(self,min_el,min_sl,max_sl):

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
            el = intersec_num
            sl = nlp.sentence_length(manswer_sent) 
            if el <= min_el or sl < min_sl or sl>max_sl :
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

    def ilp(self):
        #====> 定义问题
        prob = LpProblem("ILP for summarization problem",LpMaximize)

        #变量的字典
        x_var = []
        y_var = []

        for indx in self.entity_inverse_index:
            x_var.append("x%s"%(indx))

        for indx in self.sent_inverse_index:
            y_var.append("y%s"%(indx))

        #====> 建立variable,类别全部设为binary
        x_lpvariable = LpVariable.dicts("entity",x_var,cat=LpInteger,lowBound=0,upBound=10)
        y_lpvariable = LpVariable.dicts("sent",  y_var,cat=LpInteger,lowBound=0,upBound=1)

        #====>取得问题的实体
        title_entity = self.ep.title_entity()

        
        #获取ILP变量的权重
        def variable_weight(var):
            #首字母和尾字母
            first,last = var[0],var[1:]
            if first == "y":
                #得到句子名字
                variable_name = self.sent_inverse_index[int(last)]

                sent_entity = self.candidate_sentence_entities_dict[variable_name]

                ew = 0
                #得到句子实体数目
                el = len(sent_entity)

                for entity in self.candidate_sentence_entities_dict[variable_name]:
                    mentity_weight = self.hit_entities[entity]
                    ew += mentity_weight

                return ((el + el) + ew/2)
                
            elif first == "x":
                #得到变量实体的名字
                variable_name = self.entity_inverse_index[int(last)]
                
                #得到相应的权重
                w = self.hit_entities[variable_name]
                
                return w

            else :
                print("获取权重信息有误")
                sys.exit(1)
                

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
                ml = nlp.sentence_length(msent)
                return ml
            else:
                print("变量有问题")
                sys.exit(1)

        #满足长度限制
        prob += lpSum([y_lpvariable[i] * variable_length(i) for i in y_var]) <= self.word_limit
        prob += lpSum([y_lpvariable[i] * variable_length(i) for i in y_var]) >= (self.word_limit-100)


        #满足出现次数限制
        #对每个实体而言
        for i in range(len(self.entity_index)):
            nobj = []
            
            #对每个句子都有
            for j in range(len(self.sent_index)):
                nobj.append(self.OCC[i][j] * y_lpvariable["y%s"%(j)])

            nobj.append(-1 * x_lpvariable["x%s"%(i)])
                
            prob += lpSum( nobj ) == 0



        prob.solve()
        
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
            sent_length += nlp.sentence_length(msent)

        print("摘要长度===>",sent_length)
            
        print("权重和 = ", value(prob.objective))

        return sent_list
                

class traditional_ilp(abstract_ilp):
    def __init__(self,q,word_limit=250):
        self.ep = RFE(q,ngram,1,1,display=False,n=140,length=1600000)
        self.question = q
        abstract_ilp.__init__(self,q,word_limit,ngram,alpha=1.1,beta=15,unseen_limit=4,min_el=6,min_sl=8,max_sl=50)
        

class sparse_ilp(abstract_ilp):
    def __init__(self,q,word_limit):
        self.question = q
        nbest_total_words = 0
        nbest = q.get_nbest()
        for ans in nbest:
            content = ans.get_content()
            nbest_total_words += nlp.sentence_length(content)

        word_limit = min(int(nbest_total_words/3),150)
        self.ep = RFE(q,mngram,1,1,display=False,n=140,length=100000)
        
        abstract_ilp.__init__(self,q,word_limit,mngram,alpha=0.8,beta=15,unseen_limit=2,min_el=1,min_sl=5,max_sl=20)
        

class dis_ilp(abstract_ilp):
    def __init__(self,q,word_limit=250):

        self.question = q

        nbest_total_words = 0
        nbest = q.get_nbest()
        for ans in nbest:
            content = ans.get_content()
            nbest_total_words += nlp.sentence_length(content)

        word_limit = min(int(nbest_total_words/3),150)
        word_limit = max(10,word_limit)
        
        self.ep = RFE(q,mngram,1,1,display=False,n=140,length=100000)
        abstract_ilp.__init__(self,q,word_limit,mngram,alpha=0.8,beta=15,unseen_limit=2,min_el=1,min_sl=5,max_sl=20)
        
