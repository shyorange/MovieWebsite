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
          <td colspan="2" align="center" valign="top"><div id="Zoom">
<!--Content Start--><span style="FONT-SIZE: 12px"><td>
<p><br />[森林之子毛克利][BD-mkv.720p.中英双字][2018年剧情冒险] <br /><br /><img border="0" src="https://extraimage.net/images/2018/12/09/92335659cdfe7dbe704969414eb6adc7.jpg" alt="" /> <br /><br />◎译　　名　森林之子毛克利/丛林之书：起源/森林王子/毛克利/毛克利：魔森丛现(港)/莫格利 <br />◎片　　名　Mowgli/Jungle Book: Origins/The Jungle Book <br />◎年　　代　2018 <br />◎产　　地　美国 <br />◎类　　别　剧情/冒险 <br />◎语　　言　英语 <br />◎字　　幕　中英双字幕 <br />◎上映日期　2018-11-29(美国点映)/2018-12-07(美国) <br />◎IMDb评分　6.8/10 from 6839 users <br />◎豆瓣评分　6.3/10 from 363 users <br />◎文件格式　x264 + aac <br />◎视频尺寸　1280 x 720 <br />◎文件大小　1CD <br />◎片　　长　104分钟 <br />◎导　　演　安迪&middot;瑟金斯 Andy Serkis <br />◎编　　剧　拉迪亚德&middot;吉普林 Rudyard Kipling/Callie Kloves <br />◎主　　演　本尼迪克特&middot;康伯巴奇 Benedict Cumberbatch <br />　　　　　　克里斯蒂安&middot;贝尔 Christian Bale <br />　　　　　　凯特&middot;布兰切特 Cate Blanchett <br />　　　　　　安迪&middot;瑟金斯 Andy Serkis <br />　　　　　　娜奥米&middot;哈里斯 Naomie Harris <br />　　　　　　汤姆&middot;霍兰德 Tom Hollander <br />　　　　　　杰克&middot;莱诺 Jack Reynor <br />　　　　　　罗翰&middot;昌德 Rohan Chand <br />　　　　　　埃迪&middot;马森 Eddie Marsan <br />　　　　　　彼得&middot;穆兰 Peter Mullan <br />　　　　　　芙蕾达&middot;平托 Freida Pinto <br />　　　　　　马修&middot;瑞斯 Matthew Rhys <br />　　　　　　路易斯&middot;阿什伯恩&middot;瑟金斯 Louis Ashbourne Serkis <br /><br />◎简　　介 <br /><br />　　故事讲述了人类男孩毛克利在一片印度丛林中被狼群抚养长大。在棕熊巴鲁（Baloo）和黑豹巴希拉（Bagheera）的监护下，毛克利学习残酷的森林守则，最终被动物们接受并成为其中一员。尽管如此，他仍需要面对可怕的老虎谢利&middot;可汗（Shere Khan），毛克利的人类身世更是潜伏在森林中的巨大威胁。 <br /><br /><img border="0" src="https://lookimg.com/images/2018/12/09/cH5kn.jpg" alt="" /> <br /><br /><br /><strong><font color="#ff0000"><font size="4">【下载地址】</font></font></strong> <br /><br /><br /><a href="magnet:?xt=urn:btih:500e25052a5a2db3bfbf539fdb501b5781b3138c&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e6%a3%ae%e6%9e%97%e4%b9%8b%e5%ad%90%e6%af%9b%e5%85%8b%e5%88%a9.BD.720p.%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97%e5%b9%95.mkv&amp;tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&amp;tr=udp%3a%2f%2fthetracker.org%3a80%2fannounce&amp;tr=http%3a%2f%2fretracker.telecom.by%2fannounce"><strong><font style="BACKGROUND-COLOR: #ff9966"><font color="#0000ff"><font size="4">磁力链下载点击这里</font></font></font></strong></a></p>
<p>&nbsp;</p>
<p>
<table style="BORDER-BOTTOM: #cccccc 1px dotted; BORDER-LEFT: #cccccc 1px dotted; TABLE-LAYOUT: fixed; BORDER-TOP: #cccccc 1px dotted; BORDER-RIGHT: #cccccc 1px dotted" border="0" cellspacing="0" cellpadding="6" width="95%" align="center">
    <tbody>
        <tr>
            <td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="ftp://ygdy8:ygdy8@yg90.dydytt.net:8429/阳光电影www.ygdy8.com.森林之子毛克利.BD.720p.中英双字幕.mkv">ftp://ygdy8:ygdy8@yg90.dydytt.net:8429/阳光电影www.ygdy8.com.森林之子毛克利.BD.720p.中英双字幕.mkv</a></td>
        </tr>
    </tbody>
</table>
</p> <br><center></center>




</td>

      </tr><script language=javascript src="/js1/750.js"></script>

<br>
<font color=red>下载地址2：<a href="http://www.ygdy8.com/" target="_blank"  title="迅雷电影">点击进入</a> </font >
&nbsp; &nbsp; <font color=#07519a>温馨提示：如遇迅雷无法下载可换用无限制版尝试或用磁力下载,</font>
<font color=red><a href="/js/thunder.htm" target="_blank"  title="点击下载">点击无限制版下载！ </a> </font >
<BR><BR>
<font color=red>下载方法：安装软件后,点击即可下载,谢谢大家支持，欢迎每天来！喜欢本站,请使用Ctrl+D进行添加收藏！</font ><BR>



      <tr>
        <td colspan="2"><hr color="#CC6600" size="1px" /></td>
      </tr>
</tr>
        <center><a href="http://www.ygdy8.com/" target="_blank" ><font color="blue">点击进去首发区（第一时间更新）：想第一时间下载本站的影片吗？ </font></a>下载方法:不会下载的网友先看看"<a href=" " target="_blank" title="本站电影下载教程"><font color="blue">本站电影下载教程</font></a>"   </center>
</div>

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
    test_re();
    # print([1,2,3,4,5][1:])
