# coding=utf-8
# __author__ : "shyorange"
# __date__ :  2018/12/18
import pymysql;
from pymysql.cursors import DictCursor

class Dytt:

    def __init__(self):
        self.conn = pymysql.Connection(host="localhost",port=3306,user="root",password="root",db="firstdb",cursorclass=DictCursor);
        self.cursor = self.conn.cursor();

    # 返回数据给主页展示
    def index_get(self):
        """
        :return:
        """
        # 最新电影
        new_sql = "select movie_name,update_time from movies where movie_type like '%最新电影%' and img_link <> '暂无' order by update_time desc limit 5";
        self.cursor.execute(new_sql);
        new_movie = self.cursor.fetchall();
        # 国内电视剧
        gn_tv_sql = "select movie_name,update_time  from movies where movie_type like '%华语电视%' and img_link <> '暂无' order by update_time desc limit 5";
        self.cursor.execute(gn_tv_sql);
        gn_tv = self.cursor.fetchall();
        # 日韩剧
        rh_tv_sql = "select movie_name,update_time  from movies where movie_type like '%日韩电视%' and img_link <> '暂无' order by update_time desc limit 5";
        self.cursor.execute(rh_tv_sql);
        rh_tv = self.cursor.fetchall();
        # 欧美剧
        om_tv_sql = "select movie_name,update_time  from movies where movie_type like '%欧美电视%' and img_link <> '暂无' order by update_time desc limit 5";
        self.cursor.execute(om_tv_sql);
        om_tv = self.cursor.fetchall();
        # 总结
        all_movie = {
            "new_movie":new_movie,
            "gn_tv":gn_tv,
            "rh_tv":rh_tv,
            "om_tv":om_tv
        };
        self.__close_conn()
        return all_movie

    # 搜索返回结果
    def search_get(self,movie_name):
        """
        通过搜索寻找资源
        :param movie_name：要寻找的资源的名
        :return:
        """
        sql = f"select movie_name,update_time  from movies where movie_name like '%{movie_name}%'";
        self.cursor.execute(sql);
        res = self.cursor.fetchall();
        self.__close_conn();
        if res:
            return res;
        else:
            return None;

    def __close_conn(self):
        self.conn.commit();
        self.cursor.close();
        self.conn.close();

if __name__ == '__main__':
    dy = Dytt();
    # res = dy.search_get("海王");
    res = dy.index_get();
    print(res);