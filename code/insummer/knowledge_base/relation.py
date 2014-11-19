'''
这个文件的主要作用是弄一些关于KB的关系的处理
'''

#对relation进行一下哈希
RELATION_INDEX = {"RelatedTo":1}

#定义relation的函数集
class relation_tool:
    def __init__(self):
        pass

    def is_relation(self,rel):
        return rel.startswith('/r/')

    def is_pos(self,rel):
        rel = rel[3:]
        return not rel.startswith('Not')

    def rel_name(self,rel):
        assert self.is_relation(rel)
        if self.is_pos(rel):
            return rel[3:]
        else:
            return rel[6:]
