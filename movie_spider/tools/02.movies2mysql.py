# -*- coding=utf-8 -*-

from pyspark.sql import SparkSession
from mysql.connector import pooling

spark = SparkSession \
    .builder \
    .appName('my_app_name') \
    .getOrCreate()

'''
读取影片数据,整理后保存到数据库   
'''
json_data_1 = spark.read.json(
    "file:///D:\Projects\python_projects\movie_recommendation\douban_spider\crawl_data\douban_movies_data")
movies_data = json_data_1.select("id", "title", "cover", "url").drop_duplicates(['id'])

'''
使用spark sql语法整理数据，这里主要是字段名修改为与movies数据表一致
整理完毕后，使用write进行数据入库处理
需要注意为spark准备mysql驱动- spark下的jars目录中
'''
movies_data.registerTempTable('movies')
d = spark.sql("select id as m_id, title as m_title, cover as m_img, url as m_url from movies ")
d.write.mode("append").format("jdbc").options(
    url='jdbc:mysql://127.0.0.1:3306',
    dbtable='movies_online.movies',
    user='root',
    password='123456',
    autoReconnect=True,
    useSSL=False,
    useUnicode=True,
    characterEncoding='utf-8',
    serverTimezone='UTC',
).save()

# 合并去重后634条
