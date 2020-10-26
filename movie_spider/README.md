# 说明

## 代理ip说明
豆瓣具有反爬机制， 一个ip在爬取一定数量的数据后，就会被封，所以需要使用大量的ip proxy代理进行爬取
稳定的ip代理需要购买


## spiders

### comment_spider.py
评论数据爬取， 包含评论用户，评价电影， 评价分数

### movie_spider.py
影片数据爬取，包含爬取影片id， 影片名称，影片海报等等信息


### movie_sl_spider.py
使用selenium编写的爬虫
需要注意的是chromedriver一定要与你的浏览器版本配套

### rating_sl_spider.py
使用selenium编写的爬虫
需要注意的是chromedriver一定要与你的浏览器版本配套