#!/usr/bin/python3

import os

ddir = "/home/lavi/project/insummer/duc/Rouge_scores/"

from pprint import pprint

def main(min_rouge1f):
    total = []
    
    count = 0
    for fname in os.listdir(ddir):
        fname = ddir+fname
        f = open(fname)
        count += 1

        oner = {}
        for line in f:
            if len(line) <= 3 or line.startswith('-'):
                continue

            else:
            
                rs = line.split()
                name  = rs[1] + " " + rs[2]
                score = float(rs[3])

                oner[name] = score

        total.append(oner)

        
    print("总文档数",count)
            
    #遍历一遍找到大于rouge1f的值的所有文档
    ntotal = []
    for oner in total:
        r1f = oner["ROUGE-1 Average_F:"]
        if r1f > min_rouge1f:
            ntotal.append(oner)

    count = len(ntotal)
    ans = {'ROUGE-1 Average_R:'  :0,'ROUGE-1 Average_F:'  :0,'ROUGE-1 Average_P:'  :0,\
           'ROUGE-2 Average_R:'  :0,'ROUGE-2 Average_F:'  :0,'ROUGE-2 Average_P:'  :0,\
           'ROUGE-SU4 Average_R:':0,'ROUGE-SU4 Average_F:':0,'ROUGE-SU4 Average_P:':0,}

    print("过滤后文档数",count)
    for oner in ntotal:
        for rname in ans:
            ans[rname] += oner[rname]


    for rname in ans:
        ans[rname] /= count

    pprint(ans)


from optparse import OptionParser     
if __name__ == '__main__':
    parser = OptionParser()  
    parser.add_option("-f", "--filter", dest="rouge1",help="rouge1f最小值",default="-1")

    (options, args) = parser.parse_args()

    print("rouge1最小值",options.rouge1)

    
    main(float(options.rouge1))
