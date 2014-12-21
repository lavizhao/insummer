#coding: utf-8

'''
这个文件的主要作用是用mysql建表
'''

#表的位置
db_position = "/home/lavi/project/graduate_project/conf/db_position.conf"


from read_conf import config
import MySQLdb as mysql
import csv,sys

#设置mysql连接
conn = mysql.connect(host='localhost',user='root',passwd='',port=3306)
cur = conn.cursor()
cur.execute('use zhaoximo;')

def test_mysql():
    """
    测试mysql是否好使
    """

    count = cur.execute('show databases;')
    result = cur.fetchmany(count)
    print result
    conn.commit()

#得到建表的sql语句
def get_tb_string(tb_name):
    if tb_name == "geoname_gloss":
        return 'create table geoname_gloss(subject varchar(200),relation varchar(100), object varchar(1000))'
    elif tb_name == 'simple_types':
        return 'create table simple_types(subject varchar(300),relation varchar(300),object varchar(300) )'
    elif tb_name == "dbpedia_classes":
        return 'create table dbpedia_classes(subject varchar(500),relation varchar(300),object varchar(500) )'
    elif tb_name == "literal_facts":
        return 'create table literal_facts(id varchar(100),subject varchar(500),relation varchar(500),object varchar(500),score varchar(100))'
    elif tb_name == "facts":
        return 'create table facts(id varchar(100),subject varchar(500),relation varchar(500),object varchar(500))'
    elif tb_name == "meta_facts":
        return 'create table meta_facts(subject varchar(500) , object varchar(500), relation varchar(500), literal varchar(500),score varchar(500))'
    elif tb_name == "transitive_type":
        return 'create table transitive_type(subject varchar(500),relation varchar(500), object varchar(500))'
    elif tb_name == "types":
        return 'create table types(id varchar(200),subject varchar(500),relation varchar(500),object varchar(500))'
    elif tb_name == 'wiki_info':
        return 'create table wiki_info(subject varchar(500),relation varchar(300),object varchar(500),score varchar(200))'
    else:
        print "建表有错"
        sys.exit(1)
        
#建表
def create_table(tb_name):
    tb_string = get_tb_string(tb_name)
    cur.execute(tb_string)
    conn.commit()

#f指文件名，已经打开
#tb name指表名    
def insert_table(tb_name,f):
    reader = csv.reader(f,delimiter='\t')
    a = 0
    for line in reader:
        #print line
        value_string = get_value_string(tb_name,line)
        cur.execute('insert into %s values(%s);'%(tb_name,value_string))
        a += 1
        if a % 10000 == 0:
            conn.commit()
            print a
    conn.commit()

#傻逼的yago数据文件中有双引号的坑爹条目，给他去掉    
def get_no_quote(line):
    line = [s.replace('"','') for s in line]
    return line
    
#这个函数的作用是返回一个可以存的value        
def get_value_string(tb_name,line):
    if tb_name == "geoname_gloss":
        line = ['"'+s+'"' for s in line]
        return ','.join(line[1:len(line)-1])
        
    elif tb_name == "simple_types":
        line = get_no_quote(line)
        result = '"%s","%s","%s"'%(line[1],line[2],line[3])
        return result
        
    elif tb_name == "dbpedia_classes" :
        line = get_no_quote(line)
        result = '"%s","%s","%s"'%(line[1],line[2],line[3])
        return result
    elif tb_name == "literal_facts" :
        line = get_no_quote(line)
        result = '"%s","%s","%s","%s","%s"'%(line[0],line[1],line[2],line[3],line[4])
        return result
    elif tb_name == "facts":
        line = get_no_quote(line)
        result = '"%s","%s","%s","%s"'%(line[0],line[1],line[2],line[3])
        return result
    elif tb_name == 'meta_facts':
        line = get_no_quote(line)
        result = '"%s","%s","%s","%s","%s"'%(line[0],line[1],line[2],line[3],line[4])
        return result
    elif tb_name == 'transitive_type':
        line = get_no_quote(line)
        result = '"%s","%s","%s"'%(line[1],line[2],line[3])
        return result
    elif tb_name == "types":
        line = get_no_quote(line)
        result = '"%s","%s","%s","%s"'%(line[0],line[1],line[2],line[3])
        return result
    elif tb_name == 'wiki_info':
        line = get_no_quote(line)
        result = '"%s","%s","%s","%s"'%(line[1],line[2],line[3],line[4])
        return result
    else:
        return "fuck"
    
#删除表
def drop_table(tb_name):
    cur.execute('drop table %s'%(tb_name))

if __name__ == '__main__':
    print "您好"

    db_config = config(db_position)

    #create_geoname_gloss()
    
    #drop_table("geoname_gloss")
    #create_table('geoname_gloss')
    #insert_table("geoname_gloss",open(db_config["geoname_gloss"]))

    
    #drop_table('simple_types')
    #create_table('simple_types')
    #insert_table("simple_types",open(db_config["simple_types"]))

    #drop_table('dbpedia_classes')
    #create_table('dbpedia_classes')
    #insert_table("dbpedia_classes",open(db_config["dbpedia_classes"]))

    #drop_table('literal_facts')
    #create_table('literal_facts')
    #insert_table("literal_facts",open(db_config["literal_facts"]))

    #drop_table('facts')
    #create_table('facts')
    #insert_table("facts",open(db_config["facts"]))

    #drop_table('meta_facts')
    #create_table('meta_facts')
    #insert_table("meta_facts",open(db_config["meta_facts"]))

    #db_name = 'transitive_type'
    #drop_table(db_name)
    #create_table(db_name)
    #insert_table(db_name,open(db_config[db_name]))

    #db_name = 'types'
    #drop_table(db_name)
    #create_table(db_name)
    #insert_table(db_name,open(db_config[db_name]))

    db_name = 'wiki_info'
    drop_table(db_name)
    create_table(db_name)
    insert_table(db_name,open(db_config[db_name]))


