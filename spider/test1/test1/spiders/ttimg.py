# -*- coding: utf-8 -*-
import copy
import scrapy
from scrapy.http import Request;
from ..items import TTimgItem;

class TtimgSpider(scrapy.Spider):
    name = 'ttimg'
    allowed_domains = ['ivsky.com']
    start_urls = ['http://www.ivsky.com/tupian/ziranfengguang/']

    def parse(self, response):
        li_imgs = response.xpath('//ul[@class="ali"]/li//a');
        for detial in li_imgs:
            item = TTimgItem();
            # 分类名
            item["image_class"] = detial.xpath('./@title').extract()[0];
            # 详情页地址
            item["detail_link"] = detial.xpath('./@href').extract()[0];
            yield Request(url="http://www.ivsky.com"+item["detail_link"],meta={"item":item},callback=self.parse_detail);

    def parse_detail(self, response):
        item = response.meta["item"];
        item["image_link"] = response.xpath('//ul[@class="pli"]/li//img/@src');

        yield copy.deepcopy(item);


