# -*- coding: utf-8 -*-
import re;
import scrapy
import requests;
from lxml import etree;
from urllib.parse import unquote;
from scrapy import Request;
from ..items import TTmeiju;

class TtmeijuSpider(scrapy.Spider):
    name = 'ttmeiju'
    allowed_domains = ['meijuxz.com','']
    start_urls = ['http://www.meijuxz.com/meiju/2.html']
    base_url = 'http://www.meijuxz.com';
    html = None;
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    };

    def parse(self, response):
        a_lis = response.xpath('//a[@class="stui-vodlist__thumb lazyload"]');
        for a in a_lis:
            detail_link = self.base_url + a.xpath('./@href').extract()[0];  # 详情页连接
            # 进入详情页解析
            yield Request(url=detail_link,callback=self.parse_detail);
            # self.parse_detail(detail_link);
        # 解析下一页
        next_link = response.xpath('//a[contains(.,"下一页")]/@href').extract_first();
        if next_link:
            yield Request(url=self.base_url+next_link);

    def parse_detail(self,response):
        item = TTmeiju();
        if response:
            img = response.xpath('//div[@class="stui-content__thumb"]//img/@src');
            if img:
                item["v_img"] = img.extract()[0];
            else:
                item["v_img"] = None;
            detail = response.xpath('//div[@class="stui-content__detail"]');
            # for detail in details:
            item["v_name"] = detail.xpath('.//h3[@class="title"]/text()').extract()[0];  # 电影名
            v_actor = detail.xpath('.//p[@class="data"][1]/text()');  # 主演
            if not v_actor:
                item["v_actor"] = None;
            else:
                item["v_actor"] = v_actor.extract()[0]
            v_dir = detail.xpath('.//p[@class="data"][2]/text()');  # 导演
            if not v_dir:
                item["v_dir"] = None;
            else:
                item["v_dir"] = v_dir.extract()[0]
            v_reg = detail.xpath('.//p[@class="data"][3]/text()');  # 地区
            if not v_reg:
                item["v_reg"] = None;
            else:
                item["v_reg"] = v_reg.extract()[0]
            v_year = detail.xpath('.//p[@class="data"][4]/text()');  # 年份
            if not v_year:
                item["v_year"] = None;
            else:
                item["v_year"] = v_year.extract()[0]
            # 对简介进行简单过滤
            item["v_intr"] = re.sub(re.compile("[\'|\"]", re.S), "’",
                            response.xpath('//span[@class="detail-content"]//text()').extract()[0]);  # 简介
            # 播放视频的页面链接,通过该链接进入播放界面
            v_play_link = self.base_url + response.xpath('//a[@class="stui-vodlist__thumb picture v-thumb"]/@href').extract()[0];
            # 进入播放视频的页面，获取该电视剧的所有资源
            item["video_links"] = self.get_all_video(v_play_link);
            return item;

    # 获得网页内容的方法
    def get_html(self,url):
        for i in range(3):
            try:
                self.html = requests.get(url,headers=self.headers,timeout=7).content.decode("utf-8");
                break;
            except Exception:
                if i == 2:
                    print("获取网页失败：",url)
                    self.html = None;

    # 进入播放页面（获得对应的js文件的连接，然后访问连接，解析视频地址）
    # 可能会导致过慢。(一个个访问m3u8文件，有大量的无法访问)
    def get_all_video(self,url):
        self.get_html(url);
        if self.html:
            tre = etree.HTML(self.html);
            # 获得js文件的连接
            script_link = self.base_url+tre.xpath('//div[@class="stui-player__video embed-responsive embed-responsive-16by9 clearfix"]/script[1]/@src')[0];
            if script_link:
                # js_code = requests.get(script_link,headers=self.headers).text;
                self.get_html(script_link);
                # 获得escape加密后的视频连接
                if self.html:
                    escaped_code = re.findall(re.compile(r'.*?unescape\(\'(.*?)\'\);',re.S),self.html )[0];
                    # 进行unescape解密
                    unescaped = unquote(escaped_code.replace('%u',"\\u"),encoding='unicode-escape');
                    # 格式化视频连接，返回字典;
                    # print(unescaped)
                    video_details = re.findall(re.compile(r'.*?([第|试].*?[#|\s])', re.S),unescaped.replace('$$$', '#'));
                    if video_details:
                        video_info = {};
                        for index, video in enumerate(video_details):
                            info = video.split("$");
                            try:
                                # if语句中是继续访问m3u8文件，会导致爬取速度过慢。
                                # if ".m3u8" in info[1]:
                                #     self.get_html(info[1]);
                                #     if not self.html:
                                #         continue;
                                #     # 访问原m3u8地址，从中获取新的真实的m3u8地址
                                #     last_url = self.html.split("\n")[-1]
                                #     url_list = url.split("/");
                                #     url_list[-1] = last_url;
                                #     new_url = "/".join(url_list);
                                #     video_info[info[0]] = new_url;
                                # else:
                                video_info[info[0]] = info[1];
                            except Exception:
                                pass
                        if video_info:
                            return video_info;
                        else:
                            return None;
                    else:
                        return None;
                else:
                    return None
            else:
                return None
        else:
            return None;