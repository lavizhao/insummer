#!/usr/bin/python3
from matplotlib import pyplot as plt

wt = []
score = []
freq = []
lscore = []
lfreq = []

f = open("freq.csv")

for line in f:
    sp = line.split(',')
    if len(sp) < 2:
        continue

    else:
        sp = [float(i) for i in sp]
        wt.append(sp[0])
        score.append(sp[1])
        freq.append(sp[2])
        lscore.append(sp[3])
        lfreq.append(sp[4])
'''
fig1 = plt.figure(1)
plt.hist(wt,range=(-5,8),bins=150)
plt.xlabel('value range')
plt.ylabel('freq')
'''
'''
fig2 = plt.figure(2)
plt.hist(score,range=(0,50),bins=150)
plt.xlabel('value range')
plt.ylabel('freq')
'''
'''
fig2 = plt.figure(2)
plt.hist(freq,range=(0,150),bins=150)
plt.xlabel('value range')
plt.ylabel('freq')
'''
'''
fig2 = plt.figure(2)
plt.hist(lscore,range=(0,15),bins=150)
plt.xlabel('value range')
plt.ylabel('freq')
'''
fig2 = plt.figure(2)
plt.hist(lfreq,range=(-5,0),bins=150)
plt.xlabel('value range')
plt.ylabel('freq')



plt.show()

