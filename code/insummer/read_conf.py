#coding: utf-8
'''
这个文件的作用是将配置文件的信息以字典的形式存起来
如果是执行 python 文件名 则打印文件的所有配置信息，否则报错

'''
import sys

def config(fn):
    fn = open(fn)
    result = {}
    for line in fn.readlines():
        if len(line)<4 or line[0]=="#":
            pass
        else:
            sp = line.split()
            result[sp[0]]=sp[2]

    return result
            
if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("usage:python<input_file>")
        sys.exit(1)

    fn = sys.argv[1]
    result = config(fn)

    print(20*"=")
    print("config filename =",sys.argv[1])
    for item in result:
        print("%s = %s"%(item,result[item]))
    print(20*"=")
