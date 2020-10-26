# -*- coding=utf-8 -*-

import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:123456@localhost/movies_online?charset=utf8mb4")
# ###############################################
# pandas数据读取与入库示例
# ###############################################
# 从csv文件读取数据
users_df = pd.read_csv(r"D:\Projects\python_projects\movie_recommendation\douban_spider\analysis_data\users.csv")
'''
提取用户数据
'''
# 改列名
users_df.rename(columns={'USER_MD5':'user_md5', 'USER_NICKNAME':'nickname'}, inplace=True)
# 用户名去重
users_df.drop_duplicates(['user_md5'], keep='first', inplace=True)
# 用户名去空
users_df.dropna(subset=['nickname'], inplace=True)
# 保存到数据库 表名 users
users_df.to_sql("users", con=engine, index=False, if_exists="append")
# 从数据库读取数据
users = pd.read_sql("select * from users ", con=engine)

# ##################################
# 处理ratings数据, 保存用户名，电影id，评价数据三个字段
# #################################
rating_df = pd.read_csv(r"D:\Projects\python_projects\movie_recommendation\douban_spider\analysis_data\ratings.csv")
# 改列名
rating_df.rename(columns={'USER_MD5':'user_md5', 'RATING_ID':'rating_id', 'RATING':'rating', 'MOVIE_ID':'m_id'}, inplace=True)
# 删除无用的列
rating_df.drop(['RATING_TIME'], inplace=True, axis=1)
# 合并列表，从user_md5得到user_id
rating=pd.merge(rating_df, users, on='user_md5', how='left')
# 填充空值
import random
rating['user_id'].fillna(random.randint(1, 630000), inplace=True)
# 删除无用的列
rating.drop(['user_md5', 'nickname'], axis=1, inplace=True)
# 保存到数据库 表名 ratings
rating.to_sql("ratings", con=engine, index=False, if_exists="append")
# 从数据库读取数据
ratings = pd.read_sql("select * from ratings ", con=engine)

# ##################################
# 处理movie数据,
# #################################
movies_df = pd.read_csv(r"D:\Projects\python_projects\movie_recommendation\douban_spider\analysis_data\movies.csv",
                        usecols=['MOVIE_ID','NAME'])
movies_df.rename(columns={'MOVIE_ID':'m_id', 'NAME':'m_title'}, inplace=True)
# 完善链接
movies_df['m_url']=movies_df['m_id']
movies_df['m_url']=movies_df['m_url'].astype(str)
movies_df['m_url']='https://movie.douban.com/subject/'+movies_df['m_url'].values+'/'
movies_df['m_img']=movies_df['m_url']
# 保存到数据库 表名 movies
movies_df.to_sql("movies", con=engine, index=False, if_exists="append")


