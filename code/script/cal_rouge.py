#!/usr/bin/python3

import os

ddir = "/home/lavi/project/insummer/duc/Rouge_scores/"

rfile = list(os.walk(ddir))[0][2]

result = {}

count = 0
for one in rfile:
    fname = ddir+one
    f = open(fname)
    count += 1

    for line in f:
        if len(line) <= 3 or line.startswith('-'):
            continue

        else:
            rs = line.split()
            name  = rs[1] + " " + rs[2]
            score = float(rs[3])

            result.setdefault(name,0)
            result[name] += score

print("count",count)
            
result = sorted(result.items(),key=lambda d:d[1],reverse=True)
for i,j in result:
    if i.startswith("ROUGE-1") or i.startswith("ROUGE-2") or i.startswith("ROUGE-SU4") :
        print(i,j/count)
