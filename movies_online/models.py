# coding:utf-8
from extensions import db

ratings = db.Table('ratings', db.Column('rating_id', db.Integer, primary_key=True),
                   db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), index=True),
                   db.Column('m_id', db.Integer, db.ForeignKey('movies.m_id'), index=True),
                   db.Column('rating', db.Integer))


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128))
    user_md5 = db.Column(db.String(64))
    my_movies = db.relationship('Movies', secondary=ratings, back_populates='users')
    __table_arg__ = {
        'mysql_charset': 'utf8mb4'
    }


class Movies(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)
    m_title = db.Column(db.String(255))
    m_img = db.Column(db.String(255))
    m_url = db.Column(db.String(255))
    users = db.relationship('Users', secondary=ratings, back_populates='my_movies')
    __table_args__ = {
        'mysql_charset': 'utf8mb4'
    }
