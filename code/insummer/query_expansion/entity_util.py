#!/usr/bin/python3

'''
说明:这个文件定义了一些只有在query_expansion下才能用到的函数
'''

#Entity String 类, 这个类的作用是包含了一个字符串
#如 "get sick", get sick 可以在知识图谱中查到, sick也可以在知识图谱中查到, 所以我们取最大的集合,get sick
class entity_string:
    def __init__(self,content):
        self.__content = content

    
