# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 电影天堂的Item类
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

# 天堂图片的Item类
class TTimgItem(scrapy.Item):
    image_class = scrapy.Field();  # 图片所属的分类名
    detail_link = scrapy.Field(); # 详情页链接
    image_link = scrapy.Field(); # 详情页内每个图片的链接
    image_dir = scrapy.Field(); # 根据分类名获得文件夹名

# 天天美剧的Item类
class TTmeiju(scrapy.Item):
    v_name = scrapy.Field();    # 电影名
    v_img = scrapy.Field();     # 封面
    v_actor = scrapy.Field();   # 主演
    v_dir = scrapy.Field();     # 导演
    v_reg = scrapy.Field();     # 地区
    v_year = scrapy.Field();    # 年份
    v_intr = scrapy.Field();    # 简介
    video_links = scrapy.Field();   # 视频详情连接（视频连接或m3u8文件连接）



    
