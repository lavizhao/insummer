#!/usr/bin/python3
#coding=utf-8

'''
    为了构建ROUGE in-xml，将duc的主题和具体的评价摘要构成一个dictionary，方便构建xml
    具体就是 TOPIC-[REF-SUM] 主题：[参考摘要] 
    也就是 self-sum ： models
    duc_models path : /home/charch/gitwork/insummer/duc/duc_data/models/
    duc_topic path : /home/charch/gitwork/insummer/duc/duc_data/duc2007_testdocs/main/
'''

import os
import pickle

model_path = '/home/charch/gitwork/insummer/duc/duc_data/models'
topic_path = '/home/charch/gitwork/insummer/duc/duc_data/duc2007_testdocs/main'

topic_list = os.listdir(topic_path)
model_list = os.listdir(model_path)

duc_dict = {}

for topic in topic_list:
    for model in model_list:
        if topic[:-1] in model:
            if topic in duc_dict:
                duc_dict[topic].append(model)
            else:
                duc_dict[topic] = [model]

tm_file = open('/home/charch/gitwork/insummer/duc/duc_data/topic_model.pkl','wb')
pickle.dump(duc_dict,tm_file,True)
