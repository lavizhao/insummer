#!/usr/bin/python3
'''
说明:这里放着的就只是一个摘要的抽象类, 给看接口用的
'''
from abc import ABCMeta, abstractmethod
from ..read_conf import config
import pickle
import os

data_conf = config('../../conf/question.conf')

#Q是question类
#words是最长字数
#display是显示信息
class abstract_summarizer(metaclass=ABCMeta):
    def __init__(self,Q,words,display=False):
        self.__question = Q
        self.display = display
        self.words_limit = words

    def get_question(self):
        return self.__question

    def get_words_limit(self):
        return self.words_limit

    #抽象方法
    #返回一个sentence的list, sentence的词数之和小于word_limit.
    #现在先这么写着,到时候再换
    @abstractmethod
    def extract(self):
        pass

    #评价, 用rouge进行评价
    #两个都一样直接写在这里就好了
    def evaluation(self,result,flags):

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

    #总的接口, 外面的主要调用这个跑
    def run(self):
        #先抽
        result = self.extract()

        #计算rouge
        rouge = self.evaluation(result)

        #如果display
        if display :
            print("rouge %s"%(rouge))
