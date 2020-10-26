# -*- coding=utf-8 -*-
import re
import os
import json

'''
将爬取的影片原始数据进行规整
'''
# 取subjects部分，每一个subjects包含多部影片信息
# 即原始数据为一行包含多个影片，目标数据为一行一个影片数据
for i in range(1, 8):
    with open("../crawl_data/douban_movie_{i}".format(i=i), "r") as f:
        data = f.readlines()
        for row_line in data:
            if row_line == "\n":
                continue
            movies_data = json.loads(row_line)['subjects']
            # 保存影片数据部分， 每个影片一行数据
            with open("../crawl_data/douban_movies_data", "a") as f:
                for row_data in movies_data:
                    # 每行数据以json串格式存储
                    f.write(json.dumps(row_data))
                    f.write("\n")