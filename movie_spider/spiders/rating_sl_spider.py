# -*- coding=utf-8 -*-
import os
import re
import time
import random
import mysql.connector as connector
from selenium.webdriver.chrome.webdriver import WebDriver


cnx = connector.connect(user='root', password='123456',
                        host='localhost',database='movies_online')
cursor = cnx.cursor()
sql = "select * from movies limit 1 "
cursor.execute(sql)
res = cursor.fetchall()


browser = WebDriver(os.getcwd() +"/chromedriver")
browser.implicitly_wait(30)
# 登陆框在iframe中
browser.get("http://douban.com")
# browser.switch_to.frame(browser.find_element_by_xpath("//div[@class='login')]/iframe"))
# browser.find_element_by_class_name('account-tab-account').click()
# browser.find_element_by_id("username").send_keys("18912798378")
#
# browser.find_element_by_id("password").send_keys(".....")
# browser.find_element_by_xpath("//a[contains(@class, 'btn-account')]").click()
time.sleep(50)
for movie in res:
    time.sleep(random.randint(5,10))
    movie_url = movie[3]
    browser.get(movie_url)
    comments_count = browser.find_element_by_xpath("//div[@id='comments-section']/div/h2/span/a")
    count = re.findall('\d+', comments_count.text)[0]
    url = "https://movie.douban.com/subject/{id}/comments?start={start}&limit=20&sort=new_score&status=P"
    for start in range(0, int(count), 20):
        comments_url = url.format(id=movie[0], start=start)
        time.sleep(random.randint(5, 10))
        browser.get(comments_url)
