insummer
========

基于知识图谱的答案摘要系统

##配置

1. conf文件全部放在conf文件夹下, 这个是不外传的
2. .conceptnet5 文件夹放在/home 文件夹下
3. 讲cn\_data下的全部文件夹都考进cn_data文件夹下
4. 执行script下面的 ./data_iterates.py -t copy\_data -s
5. 装个mongo_db, 把cn\_data 下的 copy data.csv 载入到表 mongoimport -d "insunnet" -c "assertion" -f "rel,start,end,weight" -type=csv -file=fuck.csv (额, 注意表的名字)

##文件夹说明

以下文件夹均为`code/`目录下

1. `exp/` 是一些实验测试代码
2. `insummer/` 主要方法
3. `script/` 存放一些数据读写代码
4. `statistic` 存放一些统计代码
5. `test`  一些测试用代码

---------------------------------

##insummer 包文件说明

###knowledge_base

知识库接口, 封装了两个知识库, 一个是Conceptnet, 一个是Insunnet, Insunnet为我自己从Conceptnet里面抽的一部分内容

**__init__.py**

- `InsunnetFinder` 为在知识库中查找实体(关系或权重)的接口, 相当于封装了SQL
- `concept_tool` 为实体的常用工具, 例如判断两个实体是不是相等(因为会有需要判断`/c/bike` 和 `bike`相等与否的时候)

**entity_look.py**

- 查找实体相关的关系, 例如同义关系等

- `abstract_entity_lookup` 抽象类, 作为接口使用, `ConceptnetEntityLookup`和`InsunnetEntityLookup`分别为在两个知识库查找关系的类.

**relation.py**
- 定义关系, 主要作用是封装关系名, 以及判断常用函数等.

###测试代码

| 文件名        | 测试文件名     | 执行命令  |
| :------------- |:-------------| -----|
| `knowledge_base` | `test/kb.py` | `./kb.py` |














