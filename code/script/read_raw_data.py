#!/usr/bin/python3

import json
import xml
import re
import optparse
from optparse import OptionParser
import sys
sys.path.append("..")
import insummer
from insummer.common_type import Question,Answer
from insummer.read_conf import config

#抽取文件的函数,我的设想是传进去函数,然后使用函数返回调用
#question_format是个函数,通过调用返回写入文件的格式
def extract1(fn,target,question_format):
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
        if len(nbest) <=5:
            continue

        #找到问题所有标题
        title = title_re.findall(item)[0]
        #s = "问题标题 %s\n"%(title)
        
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
            
#这个是新的extract函数,主要会面对抽取json文件的工作
#fn是需要读的文件,target是目标存储文件
#question则是需要把文件存储的格式
#Question类需要使用者回去再好好看一下
#min_answer_count 是默认的最小答案数
#pass_filter 是question必须满足的条件,满足则写入
def extract(fn,target,question_format,min_answer_count=3,pass_filter=None):

    #开文件
    f = open(fn)
    t = open(target,"w")

    #indx是文件的行号
    indx,question_indx = 0,1
    title,nbest,answer_count,author = "",[],-1,""

    line = f.readline()

    while len(line) > 0:

        #先去除line两边的空格和最后结尾的逗号
        line = line.strip()

        if line[-1] == ',':
            line = line[:-1]

        #解析json
        try:
            line_json = json.loads(line)
        except:
            print("error")
            print(line)
            print("indx",indx)
            print("question indx",question_indx)
            sys.exit(1)

        #判断是问题,答案,还是错误
        if "answercount" in line_json:
            #是问题

            #先把上一个问题存了
            #content和best现阶段都是空
            #如果nbest为空,说明没有人答过,不处理
            if len(nbest) > 0:
                m_question = Question(title,"","",nbest,author,answer_count)
                #question_indx += 1

                #往文件里面写
                if m_question.get_count() > min_answer_count and \
                   pass_filter(m_question):
                    question_indx += 1
                    t.write(question_format(m_question))
                
                    if question_indx % 100 == 0:
                        print("question indx",question_indx)

            #重新计数
            if len(line_json["answercount"].strip()) > 0:
                answer_count = int(line_json["answercount"])
            else:
                answer_count = 0

            title,nbest,author = "",[],""

            #重新存
            title = line_json["subject"]
            author = line_json["postuser"]

        elif "content" in line_json :
            content = line_json["content"]
            support = int(line_json["supportnum"])
            oppose = int(line_json["opposenum"])
            ans_author = line_json["answeruser"]
            
            emp_answer = Answer(content,support,oppose,ans_author)

            nbest.append(emp_answer)

        else:
            print("error")
            sys.exit(1)

        indx += 1
        line = f.readline()
        if indx % 10000 == 0:
            print("indx",indx)

    m_question = Question(title,"","",nbest,author,answer_count)
    if m_question.get_count() > min_answer_count and \
       pass_filter(m_question):
        t.write(question_format(m_question))
            
def extract_title(tquestion):
    return tquestion.get_title()+"\n"

#将每个问题的title和best/nbest同时输出,Question[format]增加了成员函数
def extract_title1(tquestion):
    tmp_title = "---> Question <---\n" + tquestion.get_title()+"\n"
    tmp_best = "---> Best <---\n" + tquestion.get_best()+"\n"
    tmp_nbest = "---> Not Best <---\n"
    for i_dx in tquestion.get_nbest():
        tmp_nbest += ("--> NBest : " + i_dx + "\n")
    tmp = tmp_title + tmp_best + tmp_nbest
    return tmp
    #return tquestion.get_title()+"\n"


def extract_title_nbest(tquestion):
    return tquestion.get_title()+"\n"+ tquestion.get_nbest_content() + 20*"="+"\n"   
            
def get_task_function(task_string):
    if task_string == "extract_title":
        return extract_title
    elif task_string == "extract_title_nbest":
        return extract_title_nbest
    else:
        print("error in get task function")
        sys.exit(1)

def get_extract_file(task,qconf):
    result = "error"        
    if task == "extract_title":
        result = qconf["title_pos"]
    elif task == "extract_title_nbest":
        result = qconf["title_nbest_pos"]
    else:
        print("error in extract file choose")
        sys.exit(1)
    return result


#这个是这么算的,假定title10个单词
#nbest 的规定数量不是在这里算的
#假定每个nbest至少也得有5句话,要不不能进行摘要, 则每句10个单词, 那么每个答案50个单词
def word_counts_filter(question):
    #每句最少10个单词
    min_sentence_counts = 8

    min_word_counts = min_sentence_counts + len(question.get_nbest())*min_sentence_counts * 5
    if question.get_word_counts() >= min_word_counts:
        if question.get_title_words() >= min_sentence_counts:
            return True

    return False
    
def main():
    """
    主函数,-t表示什么任务
    e.g. ./read_raw_data.py -t extract_title
         ./read_raw_data.py -t extract_title_nbest
    """
    
    parser = OptionParser()  
    parser.add_option("-t", "--task",dest="task",default="error",help="你需要选择哪个任务")


    #分析命令行参数
    (options, args) = parser.parse_args()

    #检查错误
    if options.task == "error":
        print("请选择任务")
        sys.exit(1)

    #得到如何往文件里面写的格式
    task_function = get_task_function(options.task)

    #得到注册文件
    qconf = config("../../conf/question.conf")

    #得到将要写入的文件名
    extract_file = get_extract_file(options.task,qconf)

    
    #进行抽取
    extract(qconf["computer_pos"],extract_file,task_function,min_answer_count=10,pass_filter=word_counts_filter)
        
if __name__ == '__main__':
    main()
