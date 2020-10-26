# coding:utf-8
from flask import Flask, jsonify, render_template
from extensions import db, migrate
from settings import config
from models import Users, Movies
import requests

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app)


# 创建数据库命令
def register_commands(app):
    import click
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('确认要删除原来的数据库吗？', abort=True)
            db.drop_all()
            click.echo('Dropped tables.')
        db.create_all()
        click.echo('Initialized database.')


register_commands(app)


@app.route('/')
def index():
    movies_list = Movies.query.filter(Movies.m_img != None).limit(10).all()
    return render_template('index.html', movies_list=movies_list)


@app.route('/api/movies/new')
def movies_new():
    new_movies_list = Movies.query.order_by(Movies.m_id.desc()).limit(10).all()
    print('new', new_movies_list)
    return jsonify([{'m_id': movie.m_id, 'm_title': movie.m_title} for movie in new_movies_list])


@app.route('/api/movies/like')
def movies_like():
    user_id = 2  # 用户登陆则获取用户ID
    like_ids = requests.get('http://127.0.0.1:8080/api/user/{}'.format(user_id))
    print('like', like_ids.json())
    # 对like_ids可以做判断，如果返回空列表，表示推荐失败，使用其他数据替代
    # 比如使用热门数据
    like_movies_list = Movies.query.filter(Movies.m_id.in_(like_ids.json())).all()
    return jsonify([{'m_id': movie.m_id, 'm_title': movie.m_title} for movie in like_movies_list])
