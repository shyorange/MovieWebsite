from flask import Flask,render_template, redirect, url_for,request;
# 导入电影天堂数据库爬取模型
from database.models import Dytt
app = Flask(__name__)


@app.route('/')
@app.route("/index")
def index():
    movies = Dytt().index_get();
    return render_template("index.html",movies=movies);

@app.route("/category")
def category():
    """
    :param type: 类型（电影，电视剧）
    :param category: 分类名（科幻，动作，喜剧，日剧，韩剧.......）
    :param page_num: 页码，每页返回30条
    :return:leibie：哪个分类。result：该分类下的资源
    """
    # 将要根据传入的上边三个变量，进入数据库查询。
    # 需要将一下的有关数据装换为数据库中存在的。
    # 另外，还需要实现404等错误页面
    types = ["电影","电视剧","漫画","new_movies","gn_tv","rh_tv","om_tv"];
    if request.method == "GET":
        type = request.args["type"];
        category = request.args["category"];
        page_num = request.args["page_num"];
        print(type,category,page_num)
    # count：总页数，movies：资源详情
    count,movies = Dytt().category_get(type,category,page_num);
    return render_template("category.html",leibie=category,movies=movies,page_count=count);

@app.route("/robots.txt")
def robots():
    return render_template("robots.txt");

if __name__ == '__main__':
    app.run()
