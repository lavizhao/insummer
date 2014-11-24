#!/usr/bin/python3

'''
作用:遍历文件得到想要的输出
'''
import sys
sys.path.append("..")
import insummer
from insummer.read_conf import config
from insummer.knowledge_base import concept_tool
from insummer.knowledge_base.relation import relation_tool


#others
import csv
from optparse import OptionParser

conf = config("../../conf/cn_data.conf")

data_pos = conf["csv_pos"]
store_pos = conf["entity_name"]

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
def common_criterion(rel,cp1,cp2):
    if cn_tool.is_english_concept(cp1) and \
       cn_tool.is_english_concept(cp2) and \
       rel_tool.is_relation(rel):
        return True

    else:
        return False

#这个是观察结构用的
def common_print(rel,cp1,cp2):
    rel_name = rel_tool.rel_name(rel)
    if rel_name == 'HasProperty':
        print("%20s%40s%40s"%(rel_name,cp1,cp2))


    
def iter_data(function_list,store=False,display=False,store_file=None):
    triple_criterion,print_function,store_function,post_processing = function_list
    result = []
    indx = 0

    #对于某个part来说,先打开,然后再挨个统计
    #line的1,2,3 分别是relation, cp1,cp2
    for ipart in part:
        #得到指针
        reader = get_ipart_handler(ipart)

        for line in reader:
            rel,cp1,cp2 = line[1],line[2],line[3]
            #如果满足限制条件
            if triple_criterion(rel,cp1,cp2):

                if display == True:
                    print(print_function(rel,cp1,cp2))

                if store == True:
                    result.append(store_function(rel,cp1,cp2))

                indx += 1
                if indx %10000 == 0:
                    print(indx)

    if store==True:
        post_processing(result,store_file)


def entity_list_store_function(rel,cp1,cp2):
    return [cn_tool.concept_name(cp1),cn_tool.concept_name(cp2)]

def entity_list_post_function(result,store_file):
    entity_list = set()
    for cp1,cp2 in result:
        entity_list.add(cp1)
        entity_list.add(cp2)

    print("entity list %s"%(len(entity_list)))

    for cp in entity_list:
        store_file.write("%s\n"%(cp))    

#这个函数是所有task选参数            
def opt(task):
    if task == "entity_list":
        triple_criterion = common_criterion
        print_function = common_print
        store_function = entity_list_store_function
        post_processing = entity_list_post_function

    else:
        print("error")
        sys.exit(1)

    return [triple_criterion,print_function,store_function,post_processing]

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

    function_list = opt(options.task)

    if options.store == True:
        store_file = open(store_pos,"w")
        
    iter_data(function_list,display=options.display,store=options.store,store_file=store_file)
        
#这个就不用其他功能了, 省得弄得非常蛋疼    
if __name__ == '__main__':
    main()
    
