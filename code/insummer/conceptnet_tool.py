'''
这个文件的作用是封装conceptNet的一些功能,使得进行交互更为简单
'''

from .util import NLP
from conceptnet5.query import lookup

nlp = NLP()

#这个函数的作用是检测概念是否在conceptNet中,如果在则返回true, 如果不在返回false
def conceptnet_has_concept(concept):
    norm_concept = nlp.norm_text(concept)

    ans1 = lookup('/c/en/'+concept)

    indx = 0
    for item in ans1:
        indx += 1
        if indx > 0:
            break

    if indx > 0:
        return True

    ans2 = lookup('/c/en/'+norm_concept)
    indx = 0
    for item in ans2:
        indx += 1
        if indx > 0:
            break
        
    if indx > 0:
        ans1.close()        
        return True
    else:
        return False
