#KNOWLEDGE BASE 模块说明

##用途

这个模块的主要作用是对知识库进行封装. 现阶段可以利用的知识库只有ConceptNet.

##各个文件的作用

###__init__.py

concept_tool 主要封装了一些关于conceptnet中实体的常用操作, 主要函数有:
- is\_english\_concept : 判断是不是英语概念
- both\_english\_concept : 判断是不是两个概念都是英语概念
- entity\_equal : 判断实体相等的函数
- add\_prefix : 给实体加前缀, 目前是加'/c/en/', 进行了容错处理
- concept\_name : 得到实体的名字, 注意, 主要的动作是去前缀和后缀
- conceptnet\_has\_concept : 概念是否在知识库中, 现阶段是直接在知识库里面查询, 判断数量, 以后会优化

NaiveAccocSpaceWrapper 类直接移植了conceptnet的同名类, 为了修改方便的, 暂时没有什么用





