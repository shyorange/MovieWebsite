# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://movie.douban.com/']
    # start_urls = ['http://httpbin.org/get']
    # start_urls = ['https://www.baidu.com/s?wd=ip']

    def parse(self, response):
        print(response.text);
