# coding:utf-8
import os
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

# 内存不够增加spark.driver.memory
def create_spark():
    spark = SparkSession.builder.master("local[*]").appName('movie_recommend') \
        .config("spark.executor.memory", "16g").config("spark.network.timeout", "20000s")\
        .config("spark.executor.heartbeatInterval", "10000s").config('spark.driver.memory','16g')\
        .getOrCreate()
    return spark


# 从mysql读取数据
# 需要安装java sdk1.8
# 需要将资源包中的mysql-connector-java-6.0.6-bin.jar
# 文件放置到java安装环境中的jre/lib/ext目录下
def load_users(spark):
    users = spark.read.format('jdbc').options(
        url='jdbc:mysql://127.0.0.1:3306',
        dbtable='movies_online.users',
        user='root',
        password='123456',
        useSSL=False,
        useUnicode=True,
        characterEncoding='utf-8',
        serverTimezone='UTC'
    ).load()
    users.cache()  # cache结果缓存 - MERORY_AND_DISK, 相当于persist(storageLevel)默认设置
    return users


def load_movies(spark):
    movies = spark.read.format('jdbc').options(
        url='jdbc:mysql://127.0.0.1:3306',
        dbtable='movies_online.movies',
        user='root',
        password='123456',
        useSSL=False,
        useUnicode=True,
        characterEncoding='utf-8',
        serverTimezone='UTC'
    ).load()
    movies.cache()  # cache结果缓存 - MERORY_AND_DISK, 相当于persist(storageLevel)默认设置
    return movies


def load_ratings(spark):
    ratings = spark.read.format('jdbc').options(
        url='jdbc:mysql://127.0.0.1:3306',
        dbtable='movies_online.ratings',
        user='root',
        password='123456',
        useSSL=False,
        useUnicode=True,
        characterEncoding='utf-8',
        serverTimezone='UTC'
    ).load()
    ratings.cache()  # cache结果缓存 - MERORY_AND_DISK, 相当于persist(storageLevel)默认设置
    return ratings


if __name__ == '__main__':
    spark = create_spark()
    users = load_users(spark)
    movies = load_movies(spark)
    ratings = load_ratings(spark)

    users.show()
    movies.show()
    ratings.show()
