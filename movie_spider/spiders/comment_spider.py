# -*- coding=utf-8 -*-
import os
import requests
from lxml.html import document_fromstring


# 代理使用，需要购买，代理商会提供一个接口，返回可用的ip:端口
# proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
# proxies = requests.get(api_url), api_url由ip代理服务商提供，具体实现看代理商技术文档
# 示例 蓝灯翻墙代理
proxies = {'http': "http://127.0.0.1:49567", 'https': "https://127.0.0.1:49567"}
headers = {'Host': 'movie.douban.com',
 'Sec-Fetch-Dest': 'document',
 'Sec-Fetch-Mode': 'navigate',
 'Sec-Fetch-Site': 'none',
 'Sec-Fetch-User': '?1',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/85.0.4183.83 Safari/537.36'}


def get_comment_page(m_id, start):
    '''
    抓取评论页面
    :param m_id: 影片id
    :param start: 评论翻页开始数
    :return: dom
    '''
    url = "https://movie.douban.com/subject/{m_id}/comments?start={start}&limit=20&sort=new_score"
    comments_data = requests.get(url.format(m_id=m_id, start=start), headers=headers, proxies=proxies)
    dom = document_fromstring(comments_data.text)
    get_rating_data(dom, m_id)

def get_rating_data(dom, m_id):
    '''
    抓取评论数据
    :param dom: 抓取dom对象
    :param m_id: 影片id
    :return: 用户评论数据
    '''
    # 用户评论 xpath
    comment_xpath = "//span[@class='comment-info']"
    elements = dom.xpath(comment_xpath)

    lines = []
    line = ",".join(["用户昵称", "用户名", "电影ID",  "评价星级"])+"\n"
    lines.append(line)

    for ele in elements:
        nickname = ele.find("a").text_content()
        username = ele.find("a").get("href").split("/")[-2]
        rating = ele.find_class("rating")[0].get("class")[7:9]
        # 一行一条评论
        lines.append(",".join([nickname, username, str(m_id), rating])+"\n")
    with open("../crawl_data/rating.csv", "a") as f:
        f.writelines(lines)
        
if __name__ == "__main__":
    # 在有代理的情况下，无代理爬不下去
    # 从数据库读取有一条影片信息，然后从其首页抓取总的评价数量
    # 比如 rating_num = 100
    # 翻页数每页20条
    # for start in (0, rating_num, 20)即可生成翻页数
    for start in range(0, 100, 20):
        get_comment_page(m_id=3541415, start=start)
        print(start," Success")