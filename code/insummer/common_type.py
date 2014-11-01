#!/usr/bin/python3

'''
这个文件的主要作用是定义一些常见的数据结构
'''

#问题类,一个问题通常有
#1.标题 title
#2.内容,描述, content
#3.最佳答案,best
#4.所有答案,nbest
#四个部分组成

class Question:
    def __init__(self,title,content,best,nbest):
        self.__title = title
        self.__content = content
        self.__best = best
        self.__nbest = nbest
        self.type_name = "Question"

    def get_title(self):
        return self.__title    
