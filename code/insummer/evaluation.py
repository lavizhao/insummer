'''
这个文件主要做的是衡量

'''

#重合度, 就是两个set之间有多少重合的
def overlap_ratio(set1,set2):
    if len(set1)==0 or len(set2)==0:
        return 0

    return len(set1.intersection(set2)) / len(set1.union(set2))

#偏置的重合度, 就是求set1和set2的交 占set2的比例
#也就是扩充的question(也就是question和answer) 占answer的比例   
def bias_overlap_ratio(set1,set2):
    if len(set1)==0 or len(set2)==0:
        return 0

    return len(set1.intersection(set2)) / len(set2)

#实体重合数量    
def bias_overlap_quantity(set1,set2):
    if len(set1)==0 or len(set2)==0:
        return 0

    return len(set1.intersection(set2))

