# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 要爬取的数据的容器
class Test1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field();
    movie_link = scrapy.Field();
    update_time = scrapy.Field();
    # 电影分类
    movie_type = scrapy.Field(); # 一个包含分类的列表
    # 电影详情页的数据
    movie_image = scrapy.Field(); # 电影封面连接
    movie_downlink = scrapy.Field(); # 电影下载连接，一个列表

    
