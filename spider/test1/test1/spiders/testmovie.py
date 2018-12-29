# -*- coding: utf-8 -*-
import scrapy
import copy;
from ..items import Test1Item;

"""爬取电影天堂的爬虫"""

class TestmovieSpider(scrapy.Spider):
    name = 'testmovie'
    allowed_domains = ['dytt8.net','ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html','http://www.ygdy8.net/html/gndy/china/index.html','http://www.ygdy8.net/html/gndy/oumei/index.html','http://www.ygdy8.net/html/tv/hytv/index.html','http://www.ygdy8.net/html/tv/rihantv/index.html','http://www.ygdy8.net/html/tv/oumeitv/index.html']
    ## ,'http://www.ygdy8.net/html/zongyi2013/index.html'

    def parse(self, response):
        print("正在爬取：",response.url);
        # log.msg(f"正在爬取：{response.url}",level=log.ERROR);
        big_table = response.xpath('//div[@class="co_content8"]//table');
        for detail in big_table:
            item = Test1Item();
            item["movie_name"] = detail.xpath('.//a[@class="ulink"]/text()');
            item["movie_link"] = "http://www.ygdy8.net"+detail.xpath('.//a[@class="ulink"]/@href').extract()[0];
            item["update_time"] = detail.xpath('.//font/text()').extract()[0];
            # 进入详电影详情页进行解析
            yield scrapy.Request(url=item["movie_link"],meta={"item":item},callback=self.parse_detail);
        # 爬取下一页
        next = response.xpath('//a[contains(.,"下一页")]/@href').extract_first();
        if next:
            next_link = response.url[:response.url.rfind("/")+1]+next;
            yield scrapy.Request(url=next_link,callback=self.parse);

    def parse_detail(self,response):
        """
        解析详情页的方法
        :param response: 网页内容
        :return: item
        """
        item = response.meta["item"]; # 电影图片链接
        images= response.xpath('//div[@id="Zoom"]//p[1]//img');
        if not images:
            item["movie_image"] = "暂无";
        else:
            image_link = images[0].xpath('./@src').extract();
            if image_link:
                item["movie_image"] = image_link[0];
            else:
                item["movie_image"] = '暂无';
        # 电影下载链接
        down_links_div = response.xpath('//div[@id="Zoom"]//td//a/@href').extract();
        if down_links_div:
            item["movie_downlink"] = down_links_div;
        else:
            item['movie_downlink'] = '暂无';
        # 电影所属分类
        types = response.xpath('//div[@class="path"]//a/text()').extract();
        if types:
            item["movie_type"] = types[1:];
        else:
            item["movie_type"] = "暂无";
        yield item;



