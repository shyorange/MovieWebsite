#coding=gbk
#__author__ : "shyorange"
#__date__ :  2018/8/22
import time;
import random;
import sqlite3;
import requests;
from lxml import etree;
"""获取免费代理ip的工具"""
class  ProiexsPool:
    @staticmethod
    def _get_proiexs():
        # 首先爬取代理ip的网站（只爬取前两页）
        for i in range(1,10):
            html = requests.get("https://www.kuaidaili.com/free/inha/"+str(i)+"/",headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
            }).text;
            # 取出ip和协议类型
            html_tree = etree.HTML(html);
            tr_ips = html_tree.xpath("//tbody/tr");
            # print(tr_ips);
            for index,tr in enumerate(tr_ips):
                xieyi = tr.xpath("//td[4]/text()")[index];
                ip = tr.xpath("//td[1]/text()")[index]+":"+tr.xpath("//td[2]/text()")[index];
                # print(type(ip));
                # port = ;
                full_ip = {xieyi : ip};
                # 测试ip是否可用
                if ProiexsPool._check_ip(full_ip):
                    # 查看数据库中是否存在该组ip
                    if ProiexsPool._select_ip_from_database(ip):
                        # 将所有可用的ip存入数据库
                        ProiexsPool._save_ip_to_database(xieyi,ip);
            # if i == 2:
            #     break;
            # else:
            #     time.sleep(3);

    @staticmethod
    def _check_ip(ip):
        """
        检查ip是否可用的方法
        :param ip:要检查的ip
        :return: True或者False
        """
        try:
            # time.sleep(3)
            #防止出现   Max retries exceeded with url.... 错误
            # s = requests.session();
            # s.adapters.DEFAULT_RETRIES = 5;
            # s.keep_alive=False;
            print("正在检测：",ip)
            # s.proxies.update(ip);
            # s.headers= "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0";
            # html = s.get("https://movie.douban.com");
            # html = s.get("http://httpbin.org/get");
            html = requests.get("http://movie.douban.com",headers={
                "User-Agent":"User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Connection":"close"
            },proxies=ip,verify=False);
        except Exception as e:
            print("检测ip的方法报错：",e);
            return False;
        else:
            if html.status_code == 200:
                return True;
            else:
                print("该ip不可用：",html.status_code)
                return False;

    @staticmethod
    def _save_ip_to_database(xieyi,ip):
        """
        将ip存入数据库
        :param xieyi: 代理ip的协议（https，http，socket等）
        :param ip: 一个ip代理（字典类型）
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        cursor.execute("insert into proxies(xieyi ,ip) values ('{}','{}')".format(xieyi,ip));
        conn.commit();
        cursor.close();
        conn.close();

    @staticmethod
    def _select_ip_from_database(ip):
        """
        根据传入的ip查询，看数据库中是否有该ip，决定是否保存该ip
        :param ip: 要查询的ip
        :return: True或False
        """
        try:
            conn = sqlite3.connect("ProxiesPool.db");
            cursor = conn.cursor();
            cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
            count = cursor.execute("select count(ip) from proxies where ip = '{}'".format(ip));
            # print(count);
            if not count.__next__()[0]:
                return True;
            else:
                return False;
        except Exception as e:
            print(e);
        finally:
            conn.commit();
            cursor.close();
            conn.close();

    @staticmethod
    def _delete_ip_from_db(ip):
        """
        根据传入的ip删除失效的ip数据
        :param ip: 要删除的ip
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        # cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        print(ip)
        ip = ip['http'];
        print(ip)
        cursor.execute("delete from proxies where ip = '{}'".format(ip));
        conn.commit();
        cursor.close();
        conn.close();
        print("成功删除失效代理ip：{}.....".format(ip));

    @staticmethod
    def _get_random_ip():
        """
        随机获得一个ip，并检测数据库的ip数量
        :return: None
        """
        conn = sqlite3.connect("ProxiesPool.db");
        cursor = conn.cursor();
        cursor.execute("create table if not exists proxies(xieyi varchar,ip varchar)");
        counts = cursor.execute("select count(*) from proxies")
        if counts.__next__()[0] < 5:
            # 如果数据库里的ip数量小于5个，则往数据库中重新填入数据
            ProiexsPool._get_proiexs();
        # 获得数据库中所有Ip
        proxies = cursor.execute("select * from proxies");
        ips = [];
        for xieyi,ip in proxies:
            # 返回字典格式（urllib和requests使用）
            # ips.append({xieyi.lower() :xieyi.lower()+"://"+ip});
            # 返回字符串格式（scrapy使用）
            ips.append(xieyi.lower()+"://"+ip);
        conn.commit();
        cursor.close();
        conn.close();
        return random.choice(ips);



if __name__ == '__main__':
    pool = ProiexsPool();
    while True:
        ip = pool._get_random_ip();
        if pool._check_ip(ip):
            print(ip);
            break;
        else:
            pool._delete_ip_from_db(ip);