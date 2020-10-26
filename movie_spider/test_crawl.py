# -*- coding=utf-8 -*-

import os, time, random
import json
from selenium.webdriver.chrome.webdriver import WebDriver


browser = WebDriver(os.getcwd() +"/chromedriver")

url = "https://movie.douban.com/subject/34777819/comments?start=40&limit=20&sort=new_score&status=P"
browser.get(url)
comments = browser.find_elements_by_xpath("//div[@class='comment']/h3")
ratings = []
for comment in comments:
    rating = {}
    rating['m_id'] = 34777819
    rating['rating'] = comment.find_element_by_xpath("./span[2]/span[2]").get_attribute("class")[7:9]
    print(rating['rating'])
    rating['user'] = comment.find_element_by_xpath("./span[2]/a").get_attribute("href").split("/")[-2]
    print(rating['user'])
    ratings.append(rating)
print(ratings)