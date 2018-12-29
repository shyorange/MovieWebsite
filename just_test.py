# coding=utf-8
# __author__ : "shyorange"
# __date__ :  2018/12/14
import re;
import time;
import redis;
from urllib.request import Request
import urllib.request
from urllib.parse import urlencode
"""
仅仅由于测试
"""
# 测试使用redis数据库
def test_redis():
    # 获得数据库连接（decode_responses参数：为True表示插入str类型数据，为False表示插入字节数据。默认为False）
    r = redis.Redis(host="127.0.0.1",port=6379,decode_responses=True);
    # 添加一条数据
        # set(name, value, ex=None, px=None, nx=False, xx=False)
        # ex：数据过期时间（秒）
        # px：数据过期时间（毫秒）
        # nx：若设置为True，则只有当name不存在时才插入数据（新建，自动去重）
        # xx：若设置为True，则只有当name存在时才插入数据（修改）
    r.set('name',"张三");
    """
    r.setnx(); ## 添加操作，作用于set(nx=True)一样
    r.setex(name,value,time); ## 添加操作，但一段时间后自动失效（秒或timedelta对象）
    r.psetex(name,value,p_time); ## 添加，过时自动失效（毫秒或timedelta对象）
    r.mset({"sex":"女","age":"11"}); ## 批量添加，（字典或key=value形式）
    r.mget('sex','age'); ## 批量获取，（key或列表形式）
    r.getset(key，value); ## 设置新值并获取原来的值。
    r.getrange(key,start,end); ## 获取子序列，切片。（根据字节切片，非字符。汉字的截取区间必须是偶数）；
    r.setrange(name,offset,value); ## 从指定位置修改字符串内容。（offset字符串的索引，字节,一个utf8的汉字占3个字节）
    r.setbit(name,offset,value); ## 将字符串转换为二进制后，再对指定位置进行修改，value的值只能是0或1。
    r.getbit(name.,offset); ##获取指定位置的bit数据
    r.bitcount(name,start,end); ## 获取字符串二进制形式中指定区间内的1的个数
    r.delete(name); ## 删除指定key的值
    """
    print(r.getset('name','你好'));
    print(r.delete('name'));
    # 根据键取出值，两种方式都可以
    print(r["name"]);
    print(type(r["name"]));





def test_re():
    text="""
        

    """;
    com = re.compile('.*?<div id="Zoom">.*?<a href="(.*?)".*?<tbody.*?<a href="(.*?)".*?</tbody>',re.S);
    res = re.findall(com,text);
    print(res);

if __name__ == '__main__':
    # 获得一个处理代理的对象
    # prox_handle = urllib.request.ProxyHandler(prox);
    # 根据代理开启一个opener对象
    # opener = urllib.request.build_opener(prox_handle);
    # 将opener加载进urllib
    # urllib.request.install_opener(opener);
    # data = urlencode({"wd":"浏览器打不开网页"});
    # request = Request("http://www.baidu.com/s?"+data);
    # request = Request("http://down.360safe.com/setup.exe");
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.10 Safari/537.36"};
    # req = urllib.request.Request("http://down.360safe.com/setup.exe",headers=headers);
    # res = urllib.request.urlopen(req);
    # res = opener.open(request);
    # with open("360.exe","wb") as f:
    #     f.write(res);
    # res = urllib.request.urlopen("http://www.baidu.com/s?wd=ip");
    # print(res.status)
    # print(res.read().decode("utf-8"));
    # href = "http://www.ygdy8.net/html/gndy/china/list_4_2.html";
    # new = "list_4_13.html"
    # pattern = re.compile("(.*?)/")
    # print(href[:href.rfind('/')+1]+new);
    # test_re();
    # print([1,2,3,4,5][1:])
    print([1,2,3,4][-1])
