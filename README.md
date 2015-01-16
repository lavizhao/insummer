insummer
========

呵呵, 此乃机密, 老师不让说

##配置

1. conf文件全部放在conf文件夹下, 这个是不外传的
2. .conceptnet5 文件夹放在/home 文件夹下
3. 讲cn\_data下的全部文件夹都考进cn_data文件夹下
4. 执行script下面的 ./data_iterates.py -t copy\_data -s
5. 装个mongo_db, 把cn\_data 下的 copy data.csv 载入到表 mongoimport -d "insunnet" -c "assertion" -f "rel,start,end,weight" -type=csv -file=fuck.csv (额, 注意表的名字)

