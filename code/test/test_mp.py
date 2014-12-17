#!/usr/bin/python3

base = {'male', 'battery', 'barrier', 'automobile', 'admittance', 'admission', 'way', 'dobbin', 'entrée', 'access', 'nag', 'car', 'jade', 'ink', 'bung', 'vehicle', 'carload', 'railcar', 'auto_insurance', 'carriage', 'motor', 'gondola', 'electricity', 'car_battery', 'wagonload', 'entry', 'motorcar', 'auto', 'male-to-female', 'electroconvulsive_therapy', 'wagon', 'tramcar', 'plug', 'ect', 'military_battery', 'stopper', 'electric_power', 'electrical_power', 'username', 'accumulator', 'basket', 'hack'}

import sys
sys.path.append("..")
import insummer

import multiprocessing as mp

from insummer.knowledge_base import concept_tool

cn = concept_tool()

def cube(x):
    return x

import time

clock = time.time

if __name__ == '__main__':
    entity = "bike"
    
    base = list(base)
    begin = clock()
    result = cn.multi_lookup(base,entity)
    end = clock()

    time1 = end - begin

    result = []
    begin = clock()
    for ent in base:
        result.append(cn.weight_func(ent,entity))
    end = clock()

    time2 = end - begin

    print("并行 %s"%(time1))
    print("串行 %s"%(time2))
