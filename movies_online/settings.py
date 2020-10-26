# coding:utf-8

import os


class BasicConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1/movies_online?charset=utf8mb4'


class DevelopmentConfig(BasicConfig):
    pass


class ProductionConfig(BasicConfig):
    pass


config_env = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_ENV = FLASK_ENV or "development"
config = config_env[FLASK_ENV]
