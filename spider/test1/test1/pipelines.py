# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
通过textmovie文件返回的item对象被传到该文件，在该文件的process_item方法内进行数据再处理
"""
import os;
import re;
import pymysql;
# 使用redis和布隆过滤器进行电影数据去重
import redis;
from scrapy.exceptions import DropItem;
from .BloomFilter import MyBloomFilter
# 用于异步写入数据库
from pymysql import cursors;
from twisted.enterprise import adbapi;
# 导入下载图片的pipeline类
from scrapy.pipelines.images import ImagesPipeline;
from scrapy.http import Request;

# 对数据进行处理的pipeline类
class Test1Pipeline(object):
    def __init__(self):
        self.conn = redis.Redis(host='localhost',port=6379,decode_responses=True);
        self.bf = MyBloomFilter(self.conn,"movieBF",20,6);

    def process_item(self, item, spider):
        """
        将item中的数据再处理
        :param item: 主爬虫传文件传入的item对象
        :param spider: 是哪个爬虫调用该方法
        :return: 处理后item对象
        """
        if spider.name == "testmovie":
            # 判断电影名是否为空
            if not item["movie_name"]:
                raise DropItem("丢弃一个无名的影片");
            else:
                item["movie_name"] = item["movie_name"].extract()[0];
            if len(item["movie_name"]) <8:
                raise DropItem();
            elif item["movie_downlink"] == "暂无":
                raise DropItem();
            # 判断电影是否已经爬取过，将已经爬取过的电影进行丢弃
            if self.bf.is_exists(item["movie_name"]):
                raise DropItem(f"该电影已爬取过：{item['movie_name']}");
            else:
                self.bf.insert(item["movie_name"]);
            # 将电影详情页连接拼接完整
            item["movie_link"] = "http://www.ygdy8.net"+item["movie_link"];
            # 将更新时间里的\r\n去除，并去除其他无用数据
            update_time = item["update_time"].replace('\r','').replace('\n','');
            com = re.compile('.*?日期：(.*?)点击.*?',re.S);
            new_time = re.findall(com,update_time);
            if new_time:
                item["update_time"] = new_time[0];
            else:
                item["update_time"] = None;
        elif spider.name == "ttimg":
            pass
        return item

# 将数据保存到mysql的pipeline类
# 异步写入
class MySQLASCYPipeline:

    def __init__(self,db_pool):
        # 连接数据库需要的各参数
        # self.host = host;host,port,user,password,db,charset,
        # self.port = port;
        # self.user = user;
        # self.password = password;
        # self.db = db;
        # self.charset = charset;
        self.db_pool = db_pool;


    # scrapy内置方法，不能随便修改名字和参数
    @classmethod
    def from_settings(cls,settings):
        """
        一个类方法，在init函数之前执行，并返回参数给init函数（用于从settings文件中获取配置信息）
        :param crawler: 通过该变量可以获得整个scrapy的所有配置信息
        :return: init函数需要的一切参数
        """
        db_params = dict(
            host=settings.get('HOST'),
            port=settings.get('PORT'),
            user=settings.get('USER'),
            password=settings.get('PASSWORD'),
            db=settings.get('DB'),
            # charset=crawler.settings.get('CHARSET'),
            cursorclass=cursors.DictCursor,
        );
        # 创建一个连接池
        db_pool = adbapi.ConnectionPool('pymysql',**db_params);
        return cls(db_pool);

    def process_item(self,item,spider):
        """
        处理item中的数据的方法，（将数据保存到数据）
        :return: item（传给下一个pipeline类）
        """
        if spider.name == "testmovie":
            # 把插入数据的方法和要插入的数据放入连接池
            query = self.db_pool.runInteraction(self.insert_into_dytt,item);
            # 如果插入数据发生错误，则自动回调该方法(传入处理错误的函数，出错的item，和哪个爬虫)
            query.addErrback(self.handle_error,item,spider);
            return item;
        elif spider.name == "ttmeiju":
            query = self.db_pool.runInteraction(self.insert_into_ttmeiju, item);
            query.addErrback(self.handle_error, item, spider);
            return item;

    # 插入电影天堂表
    def insert_into_dytt(self,cursor,item):
        sql = f'insert into dytt_movies(movie_name, movie_type,img_link,down_link,update_time) values ("{item["movie_name"]}","{item["movie_type"]}","{item["movie_image"]}","{item["movie_downlink"]}","{item["update_time"]}")';
        cursor.execute(sql);

    # 插入天天美剧表
    def insert_into_ttmeiju(self,cursor,item):
        sql = f"""insert into ttmeiju (v_name,v_reg,v_actor,v_dir,v_year,v_img,v_intr,video_links) values('{item["v_name"]}','{item["v_reg"]}','{item["v_actor"]}','{item["v_dir"]}','{item["v_year"]}','{item["v_img"]}','{item["v_intr"]}',"{item["video_links"]}")""";
        print("*************",sql)
        cursor.execute(sql);


    def handle_error(self,failure,item,spider):
        print(spider.name," 爬虫存数据出错：",failure)

# 非异步写入
class MySQLPipeline(object):
    def __init__(self, conn):
        self.conn = conn;

    # 从数据库获取连接mysql的相关信息
    @classmethod
    def from_settings(cls,settings):
        db_params = dict(

            # charset=crawler.settings.get('CHARSET'),
        );
        # 连接数据库
        conn = pymysql.Connection(host=settings.get('HOST'),
            port=settings.get('PORT'),
            user=settings.get('USER'),
            password=settings.get('PASSWORD'),
            db=settings.get('DB'),
            cursorclass=cursors.DictCursor,);
        return cls(conn);

    # 爬虫启动时调用
    #   scrapy内置的方法，方法名不能修改，参数不能添加或减少
    def open_spider(self,spider):
        """
        该方法是一个scrapy内部的方法，当爬虫启动时调用该方法（进行连接数据库和建表）
        :param spider: 当前是哪个爬虫
        :return: None
        """
        # self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset=self.charset,cursorclass=cursors.DictCursor);
        if spider.name == "testmovie":
            self.cursor = self.conn.cursor();
            # 建表
            sql = 'create table if not exists movies(id integer primary key auto_increment, movie_name varchar(100) not null default "暂无", movie_type varchar(200) not null  default "暂无",img_link varchar(200) not null default "暂无",down_link varchar(6000) not null default "暂无",update_time varchar(100) not null default "暂无")';
            self.cursor.execute(sql);
            self.conn.commit();

    def process_item(self,item,spider):
        if spider.name == "testmovie":
            sql = f'insert into movies(movie_name, movie_type,img_link,down_link,update_time) values ("{item["movie_name"]}","{item["movie_type"]}","{item["movie_image"]}","{item["movie_downlink"]}","{item["update_time"]}")';
            self.cursor.execute(sql);
            self.conn.commit();
        return item;
# 爬虫关闭时调用
#   scrapy内置的方法，方法名不能修改，参数不能添加或减少
    def close_spider(self,spider):
        """
        当爬虫关闭时调用该方法，（用来关闭数据库连接）
        :param spider: 当前是哪个爬虫
        :return: None
        """
        if spider.name == "testmovie":
            self.conn.commit();
            self.cursor.close();
            self.conn.close();

# 下载天堂图片的Pipeline类
class DownTTIMagePipeline(object):
    def __init__(self):
        # 将图片下载到哪个文件夹
        self.image_dirs = "D:/ScrapyDownImages/TianTangImages/";

    def get_media_requests(self,item,info):
        for img_url in item["image_link"]:
            yield Request(img_url,meta={"item":item});

    def file_path(self,request,response=None,info=None):
        """
        返回图片的详细下载位置
        """
        # 以图片分类为名创建文件夹
        img_dir = request.meta["item"]['image_class'];
        if not os.path.exists(self.image_dirs+img_dir):
            os.mkdir(self.image_dirs+img_dir);
        # 根据图片链接获得图片名
        image_name = request.url.split("/")[-1];
        # 图片的完成路径
        path = self.image_dirs+img_dir+image_name;

        return path

    def item_completed(self,results,item,info):
        """
        图片下载完成后的结果
        """
        image_path = [x["path"] for ok,x in results if ok];
        if not image_path:
            raise DropItem("该item里没图片");
        return item;

