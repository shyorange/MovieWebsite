from flask import Flask,render_template, redirect, url_for,request;
# 导入电影天堂数据库爬取模型
from database.models import Dytt
app = Flask(__name__)


@app.route('/')
@app.route("/index")
def index():
    movies = Dytt().index_get();
    return render_template("index.html",movies=movies);


if __name__ == '__main__':
    app.run()
