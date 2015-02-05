#!/usr/bin/python3
#coding=utf-8

'''
    python script for ROUGE-1.5.5
    不同于之前的指定要待测list和reflist的list，
    这里我们只能指定两个目录地址，待测的所有sum和对应的所有ref
    利用topic来寻找指定的evalID,Peer,models
'''

import os
import re
import pickle

# input : 
    # all summarization's path.
    # all the referance summarization's path
# output :
    # the rouge eval scores

def pythonROUGE(sum_path,ref_path):
    '''func to use the interface of rouge.'''
    '''
        大概过程就是，对sum_path中的每个sum，从ref中找到对应的ref_sum然后创建一个临时的xml输入
        传入到rouge中，进行scoring，然后输出
        这个xml可以直接全部构成，所以传入的还是path+path
    '''
    xml_path = '/home/charch/gitwork/insummer/duc/lexrank.xml'
    xml_file = open(xml_path,'w')
    create_xml(xml_file,sum_path,ref_path)

    ROUGE_path = '/home/charch/gitwork/insummer/duc/RELEASE-1.5.5/ROUGE-1.5.5.pl'
    data_path = '/home/charch/gitwork/insummer/duc/RELEASE-1.5.5/data'

    options = ' -n 4 -w 1.2 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -a '#-d rougejk.in'
    #options = '-a -m -n 2'

    ROUGE_output_path = '/home/charch/gitwork/insummer/duc/ROUGE_result'

    #exec_command = ROUGE_path + ' -e ' + data_path + ' ' + options + ' -x ' + xml_path + ' > ' + ROUGE_output_path
    exec_command = ROUGE_path + ' -e ' + data_path + options + '-x ' + xml_path + ' > ' + ROUGE_output_path

    os.system(exec_command)


def create_xml(xml_file,sum_path,ref_path):
    '''根据所有待rouge的sum产生一个完整的xml'''
    '''
        大概结构
        <version ...>
        repeat:
        <evalID ..>
        <peers path>
        <model path>
        <peers>
        <models>
    '''

    xml_file.write('<ROUGE_EVAL version="1.5.5">\n')

    peers_path = '/home/charch/gitwork/insummer/duc/sum_result/lexrank_rank'
    #peers_path = '/home/charch/gitwork/insummer/duc/sum_result/lexrank_rank'
    model_path = '/home/charch/gitwork/insummer/duc/duc_data/models'

    
    #得到sum和ref对应关系，就是topic和assessor的对应关系
    sum_ref = '/home/charch/gitwork/insummer/duc/duc_data/topic_model.pkl'
    sr_file = open(sum_ref,'rb')
    topic_ass_dict = pickle.load(sr_file)

    #然后是遍历所有的sum，按其主题再遍历所有对应的ref（一个做evalID，其余做models）
    #每个主题都产生四个，evalID不同，但是peers同

    sum_list = os.listdir(sum_path)

    for peer in sum_list:
        for evalid in topic_ass_dict[peer]:
            #the rest is the models
            xml_file.write('<EVAL ID="' + evalid + '">\n')
            xml_file.write('<PEER-ROOT>\n')
            xml_file.write(peers_path + '\n')
            xml_file.write('</PEER-ROOT>\n')
            xml_file.write('<MODEL-ROOT>\n')
            xml_file.write(model_path + '\n')
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
            

if __name__ == "__main__":
    sum_path = '/home/charch/gitwork/insummer/duc/sum_result/lexrank_rank/'
    ref_path = '/home/charch/gitwork/insummer/duc/duc_data/models/'

    pythonROUGE(sum_path,ref_path)
