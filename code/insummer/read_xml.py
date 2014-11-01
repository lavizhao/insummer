#!/usr/bin/python3

import xml
import re
import optparse
from read_conf import config
from optparse import OptionParser
import sys

from common_type import Question


#抽取文件的函数,我的设想是传进去函数,然后使用函数返回调用
#question_format是个函数,通过调用返回写入文件的格式
def extract(fn,target,question_format):
    #开文件
    t = open(target,"w")

    #读全部数据
    print("读数据...")
    xf = open(fn).readlines()
    xf = ' '.join(xf)

    #这是搜寻素有问题的re
    question_re = re.compile(r"<vespaadd>(.+?)</vespaadd>",re.DOTALL)

    #搜寻问题title的re
    title_re = re.compile(r"<subject>(.+?)</subject>",re.DOTALL)

    #问题内容(描述)的ren
    content_re = re.compile(r"<content>(.+?)</content>",re.DOTALL)

    #最佳答案的re
    best_re = re.compile(r"<bestanswer>(.+?)</bestanswer>",re.DOTALL)

    #全部答案的re
    nbest_re = re.compile(r"<answer_item>(.+?)</answer_item>",re.DOTALL)

    #找到所有的问题
    result = question_re.findall(xf)

    #对找到的正则开始处理
    #indx是索引,item是全部问题的raw格式, 也就是带tag的形式
    print("开始处理...")
    for indx,item in enumerate(result):

        #抽取全部答案, 后面有判断答案数量, 这个在后期会有所修改
        nbest = nbest_re.findall(item)
        if len(nbest) <=1:
            continue

        #找到问题所有标题
        title = title_re.findall(item)[0]
        s = "问题标题 %s\n"%(title)
        
        content = content_re.findall(item)
        if len(content)!=0:
            content = content[0]
        else:
            content = ""
        
        best = best_re.findall(item)[0]

        #title,content,best,得到的均是字符串,nbest得到的是一个数组

        new_question = Question(title,content,best,nbest)

        t.write(question_format(new_question))
        
        #print("%s"%(50*"="))

        if indx%1000 == 0:
            print(indx)

def extract_title(tquestion):
    return tquestion.get_title()+"\n"
            
def get_task_function(task_string):
    if task_string == "extract_title":
        return extract_title
    else:
        print("error in get task function")
        sys.exit(1)

def main():
    """
    主函数,-t表示什么任务
    """
    
    parser = OptionParser()  
    parser.add_option("-t", "--task",dest="task",default="error",help="你需要选择哪个任务")

    (options, args) = parser.parse_args()

    if options.task == "error":
        print("请选择任务")
        sys.exit(1)

    task_function = get_task_function(options.task)

    qconf = config("../../conf/question.conf")

    extract(qconf["question_pos"],qconf["title_pos"],task_function)
        
if __name__ == '__main__':
    main()
