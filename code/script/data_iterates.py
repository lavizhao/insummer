#!/usr/bin/python3

'''
作用:遍历文件得到想要的输出
'''
import csv
import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config
from insummer.knowledge_base import concept_tool
from insummer.knowledge_base.relation import relation_tool

import pickle

from abc import ABCMeta, abstractmethod

#others
import csv
from optparse import OptionParser

conf = config("../../conf/cn_data.conf")

data_pos = conf["csv_pos"]

part = [i for i in range(0,8)]

cn_tool = concept_tool()
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
def common_criterion(line):
    rel,cp1,cp2,weight = line[1],line[2],line[3],line[5]    
    if cn_tool.is_english_concept(cp1) and \
       cn_tool.is_english_concept(cp2) and \
       rel_tool.is_relation(rel) and \
       float(weight) >0 and rel_tool.is_pos(rel):
        return True

    else:
        return False

#这个是观察结构用的
def common_print(line):
    rel,cp1,cp2 = line[1],line[2],line[3]    
    rel_name = rel_tool.rel_name(rel)
    if rel_name == 'HasProperty':
        print("%20s%40s%40s"%(rel_name,cp1,cp2))
    
def iter_data(func,store=False,display=False):
    result = []
    indx = 0

    #对于某个part来说,先打开,然后再挨个统计
    #line的1,2,3 分别是relation, cp1,cp2
    for ipart in part:
        #得到指针
        reader = get_ipart_handler(ipart)

        for line in reader:
            #如果满足限制条件
            if func.get_triple_criterion()(line):

                if display == True:
                    print(func.get_print_function()(line))

                if store == True:
                    result.append(func.get_store_function()(line))

                indx += 1
                if indx %10000 == 0:
                    print(indx)

    if store==True:
        func.get_post_processing()(result)


class abstract_func(metaclass=ABCMeta):
    def __init__(self,store):
        self.__store = store

    def is_store(self):
        return self.__store
        
    def get_print_function(self):
        return self.print_function

    def get_triple_criterion(self):
        return self.triple_criterion

    def get_store_function(self):
        return self.store_function

    def get_post_processing(self):
        return self.post_processing

    @abstractmethod
    def print_function(self,line):
        pass

    @abstractmethod
    def triple_criterion(self,line):
        pass

    @abstractmethod
    def store_function(self,line):
        pass

    @abstractmethod
    def post_processing(self,result):
        pass
        
class entity_list_func(abstract_func):
    def __init__(self,store):
        abstract_func.__init__(self,store)
        self.__name = "entity_list"
        
    def print_function(self,line):
        return common_print(line)

    def triple_criterion(self,line):
        return common_criterion(line)

    def store_function(self,line):
        rel,cp1,cp2 = line[1],line[2],line[3]    
        return [cn_tool.concept_name(cp1),cn_tool.concept_name(cp2)]

    def post_processing(self,result):
        if self.is_store()==False:
            return
            
        store_file = open(conf[self.__name],"wb")    
        entity_list = set()
        for cp1,cp2 in result:
            entity_list.add(cp1)
            entity_list.add(cp2)

        print("entity list %s"%(len(entity_list)))

        #for cp in entity_list:
        #    store_file.write("%s\n"%(cp))
        pickle.dump(entity_list,store_file,True)

class copy_data(abstract_func):
    def __init__(self,store):
        abstract_func.__init__(self,store)
        self.__name = "copy_data"
        store_file = open(conf[self.__name],"w")
        self.writer = csv.writer(store_file)
        
    def print_function(self,line):
        return common_print(line)

    def triple_criterion(self,line):
        return common_criterion(line)

    def store_function(self,line):
        rel,cp1,cp2,weight=line[1],line[2],line[3],line[5]
        
        rel = rel_tool.rel_name(rel)
        cp1,cp2 = cn_tool.concept_name(cp1),cn_tool.concept_name(cp2)
        
        
        result = [rel,cp1,cp2,weight]    
        self.writer.writerow(result)
        return 1

    def post_processing(self,result):
        return 
        
#这个函数是所有task选参数            
def opt(task,store):
    if task == "entity_list":
        return entity_list_func(store)

    elif task == "copy_data":
        return copy_data(store)
        
    else:
        print("error")
        sys.exit(1)

def main():
    '''
    task ./data_iterates -t entity -s
    '''

    parser = OptionParser()  
    parser.add_option("-t", "--task",dest="task",default="error",help="你需要选择哪个任务")
    parser.add_option("-s", "--store",dest="store",action="store_true",help="选择存储与否",default=False)
    parser.add_option("-d", "--display",dest="display",action="store_true",help="选择显示与否",default=False)

    #分析命令行参数
    (options, args) = parser.parse_args()

    #检查错误
    print(options)
    if options.task == "error":
        print("请选择任务")
        sys.exit(1)

    func = opt(options.task,options.store)

    iter_data(func=func,display=options.display,store=options.store)
        
#这个就不用其他功能了, 省得弄得非常蛋疼    
if __name__ == '__main__':
    main()
    
