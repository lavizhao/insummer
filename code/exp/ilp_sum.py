#!/usr/bin/python3

'''
看看原始摘要的效果
'''

import sys,os
sys.path.append("..")
import insummer

import pickle
from insummer.read_conf import config

import data
import logging
from optparse import OptionParser 

from insummer.summarization.ilp import traditional_ilp as TI
data_conf = config('../../conf/question.conf')

def write_tofile(question,sent_list):
    
    wp = data_conf["ilp_sum"]
    wp += question.get_author()
    wp = wp[:-1]

    f = open(wp,"w")
    for msent in sent_list:
        f.write(msent+" ")

    f.close()
    return wp    


def evaluation(result,flags):

    xml_file = open(data_conf['xml_path'],'w')
    xml_file.write('<ROUGE_EVAL version="1.5.5">\n')
    topic_ass_dict = pickle.load(open(data_conf['topic_ass_path'],'rb'))
    tmp_s = result.split('/')
    peer = tmp_s[-1]
    score_path = data_conf['ROUGE_SCORE']+peer+flags
    peer_path = '/'.join(tmp_s[:-1])
    for evalid in topic_ass_dict[peer]:
        xml_file.write('<EVAL ID="' + evalid + '">\n')
        xml_file.write('<PEER-ROOT>\n')
        xml_file.write(peer_path + '\n')
        xml_file.write('</PEER-ROOT>\n')
        xml_file.write('<MODEL-ROOT>\n')
        xml_file.write(data_conf['ROUGE_model'] + '\n')
        xml_file.write('</MODEL-ROOT>\n')
        xml_file.write('<INPUT-FORMAT TYPE="SPL">\n')
        xml_file.write('</INPUT-FORMAT>\n')
        xml_file.write('<PEERS>\n')
        xml_file.write('<P ID="'+ peer[3:5] +'">' + peer + '</P>\n')
        xml_file.write('</PEERS>\n')
        xml_file.write('<MODELS>\n')
        for s_model in topic_ass_dict[peer]:
            if s_model != evalid:
                xml_file.write('<M ID="' + s_model[-1] + '">' + s_model + '</M>\n')
        xml_file.write('</MODELS>\n')
        xml_file.write('</EVAL>\n')
    xml_file.write('</ROUGE_EVAL>')
    xml_file.close()

    options = ' -n 4 -w 1.2 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -a '

    exec_command = data_conf['ROUGE_PATH'] + ' -e ' + data_conf['rouge_data_path'] + options + ' -x ' + data_conf['xml_path'] + ' > ' + score_path

    os.system(exec_command)



#定义exp函数, 是实验的主体
#qnum是问题数据的个数
def exp(questions,qnum):

    for i in range(qnum):
        print("问题 %s"%(i))
        q = questions[i]
        q.clean()
        ose = TI(q,250)

        slist = ose.extract()

        wp = write_tofile(ose.get_question(),slist)

        evaluation(wp,'ilp')
        print(100*"=")

if __name__ == '__main__':
    print(__doc__)

    parser = OptionParser()  
    parser.add_option("-d", "--data", dest="data",help="选择数据集")

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
        
    exp(questions,len(questions))
        
