'''
这个文件的主要作用是弄一些关于KB的关系的处理
'''

#定义各个relation的编号, 为了后续使用, 这样以后定义关系的时候基本上使用哈希的方法来写
#这个方法实现的非常丑, 但是我又没有别的办法了

REL_INDX = {\
            'RelatedTo':0,\
            'PartOf':1,\
            'ReceivesAction':2,\
            'EtymologicallyDerivedFrom':3,\
            'MotivatedByGoal':4,\
            'HasLastSubevent':5,\
            'HasPrerequisite':6,\
            'HasContext':7,\
            'InstanceOf':8,\
            'CapableOf':9,\
            'HasProperty':10,\
            'CausesDesire':11,\
            'Synonym':12,\
            'HasSubevent':13,\
            'DefinedAs':14,\
            'HasA':15,\
            'Desires':16,\
            'Attribute':17,\
            'DerivedFrom':18,\
            'IsA':19,\
            'Causes':20,\
            'HasFirstSubevent':21,\
            'MemberOf':22,\
            'MadeOf':23,\
            'UsedFor':24,\
            'wordnet/adjectivePertainsTo':25,\
            'wordnet/adverbPertainsTo':26,\
            'SimilarTo':27,\
            'AtLocation':28,\
            'Antonym':29,\
            'other':30,\
        }

#定义relation的函数集
class relation_tool:
    def __init__(self):
        #包含synonym,DefinedAs,DerivedFrom
        self.__synonym_type = {12,14,18}
        #self.__synonym_type = {12,14}
        self.__relate_type = {0}

    #检测概念是否是关系
    
    def is_relation(self,rel):
        rel = self.rel_name(rel)
        if rel == 'other':
            return False
        return rel in REL_INDX.keys()

    #是不是positive
    def is_pos(self,rel):
        assert self.is_relation(rel)
        if rel.startswith('/r'):
            rel = rel[3:]
            return not rel.startswith('Not')
        else:
            assert self.is_relation(rel)
            return True

    def rel_name(self,rel):
        if rel.startswith('/r/Not'):
            return rel[6:]
        elif rel.startswith('/r'):
            return rel[3:]
        else:
            return rel    

    def get_rel_indx(self,rel_name):
        indx = -1
        rel_name = self.rel_name(rel_name)
        if rel_name in REL_INDX:
            return REL_INDX[rel_name]
        else:
            return REL_INDX['other']
        
    #得到关系的具体函数
    def get_rel_type(self,rel,type_set):
        rel_name = self.rel_name(rel)
        rel_indx = self.get_rel_indx(rel_name)
        if rel_indx in type_set:
            return True
        else:
            return False

    #同义词关系函数
    def synonym_type(self,rel):
        return self.get_rel_type(rel,self.__synonym_type)

    #关联关系
    def relate_type(self,rel):
        return self.get_rel_type(rel,self.__relate_type)
        
rel_tool = relation_tool()

            
