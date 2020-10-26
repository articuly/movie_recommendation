# -*- coding=utf-8 -*-
import os, time, random
import json
from selenium.webdriver.chrome.webdriver import WebDriver

# 谷歌浏览器驱动
browser = WebDriver(os.getcwd() +"/chromedriver")

def get_json(url):
    browser.get(url)
    json_str = browser.find_element_by_xpath("//body/pre").text
    f.write(json_str+"\n")


# 最新的影片
urls = [
    "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&" \
    "page_limit=20&page_start={0}".format(index)
    for index in range(474, 499)
]

# # 最热的影片
# urls = [
#     "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&" \
#     "page_limit=20&page_start={0}".format(index)
#     for index in range(401)
# ]

with open("../crawl_data/douban_new_url", "a") as f:
    for url in urls:
        time.sleep(random.randint(5, 10))
        get_json(url)
