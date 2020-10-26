# -*- coding=utf-8 -*-
import time
import random
import requests
from lxml.html import document_fromstring

# 代理
proxies = {'http': "http://127.0.0.1:49567", 'https': "https://127.0.0.1:49567"}
tags = [
    "%E7%83%AD%E9%97%A8",
    "%E6%9C%80%E6%96%B0",
    "%E7%BB%8F%E5%85%B8",
    "%E5%8F%AF%E6%92%AD%E6%94%BE",
    "%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86",
    "%E5%86%B7%E9%97%A8%E4%BD%B3%E7%89%87",
    "%E5%8D%8E%E8%AF%AD",
    "%E6%AC%A7%E7%BE%8E",
    "%E9%9F%A9%E5%9B%BD",
    "%E6%97%A5%E6%9C%AC",
    "%E5%8A%A8%E4%BD%9C",
    "%E5%96%9C%E5%89%A7",
    "%E7%88%B1%E6%83%85",
    "%E7%A7%91%E5%B9%BB",
    "%E6%82%AC%E7%96%91",
    "%E6%81%90%E6%80%96",
    "%E5%8A%A8%E7%94%BB"

]

headers = {
"Host": "movie.douban.com",
"Referer": "https://movie.douban.com/explore",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"
}


movie_url = "https://movie.douban.com/j/search_subjects?type=movie&tag={tag}" \
      "&sort=time&page_limit=20&page_start={start}"

for start in range(60):
    time.sleep(random.randint(4,8))
    url = movie_url.format(tag=tags[0], start=start)
    # 注意ip代理可用性
    data = requests.get(url, headers=headers, proxies=proxies)
    print(data.text)
    with open("../crawl_data/douban_new_url", "a") as f:
        f.write(data.text+"\n")