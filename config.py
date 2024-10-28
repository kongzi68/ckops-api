# coding=utf-8
import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
log_config = {
    'LOG_DIR': '/var/log/ck_ops/',
    'LOG_CONFIG': 'ops/libs/logging.yaml',
    'LOG_LEVEL': 'INFO'
}

# db配置
db_ops = {
    "dev": {
        'host': 'iamIPaddr',
        'port': 3306,
        'dbname': 'ck_ops',
        'user': 'username',
        'passwd': 'iampassword'
    },
    "test": {
        'host': 'iamIPaddr',
        'port': 3306,
        'dbname': 'ck_ops',
        'user': 'username',
        'passwd': 'iampassword'
    },
    "pro": {
        'host': 'iamIPaddr',
        'port': 3306,
        'dbname': 'ck_ops',
        'user': 'username',
        'passwd': 'iampassword'
    }
}


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MqUYFVFZkQeZoEx9qWRLrLYSs9igvskOmCun1KmZ'
    TOKEN_EXPIRATION = int(os.environ.get('TOKEN_EXPIRATION') or 600)
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    # db库
    db_engine_url = URL('mysql+pymysql',
                        username=db_ops['dev']['user'],
                        password=db_ops['dev']['passwd'],
                        host=db_ops['dev']['host'],
                        port=db_ops['dev']['port'],
                        database=db_ops['dev']['dbname']
                        )

    # 数据库
    """
    # cmdb_web_engine_url 对象类型为 class
    # SQLALCHEMY_DATABASE_URI = cmdb_web_engine_url
    # 因 flask_migrate 需要的 SQLALCHEMY_DATABASE_URI 数据类型为字符串
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:iamIPaddr.iamIPaddr/cmdb_web?charset=utf8"
    SQLALCHEMY_DATABASE_URI = cmdb_web_engine_url
    SQLALCHEMY_BINDS = {
        'cmdb': cmdb_engine_url,
        'cmdb_oss': cmdb_oss_engine_url}
    """
    SQLALCHEMY_DATABASE_URI = db_engine_url.__to_string__(hide_password=False)

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    db_engine_url = URL('mysql+pymysql',
                        username=db_ops['test']['user'],
                        password=db_ops['test']['passwd'],
                        host=db_ops['test']['host'],
                        port=db_ops['test']['port'],
                        database=db_ops['test']['dbname']
                        )
    SQLALCHEMY_DATABASE_URI = db_engine_url.__to_string__(hide_password=False)


class ProductionConfig(Config):
    db_engine_url = URL('mysql+pymysql',
                        username=db_ops['pro']['user'],
                        password=db_ops['pro']['passwd'],
                        host=db_ops['pro']['host'],
                        port=db_ops['pro']['port'],
                        database=db_ops['pro']['dbname']
                        )
    SQLALCHEMY_DATABASE_URI = db_engine_url.__to_string__(hide_password=False)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
