# coding: utf-8
import os

from dotenv import dotenv_values

env = {
    **dotenv_values(".env"),
    **os.environ
}

basedir = os.path.abspath(os.path.dirname(__file__))

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [%(process)d] [%(funcName)s] [%(lineno)s]:%(message)s',
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': './logs/apps.log',
            'formatter': 'verbose',
        },
        "request": {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': './logs/requests.log',
            'formatter': 'verbose',
        },
        "error": {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': './logs/error.log',
            'formatter': 'verbose',
        },

    },
    "loggers": {
        "app": {
            'level': 'INFO',
            'handlers': ['default'],
            'propagate': True
        },
        "request": {
            'level': 'INFO',
            'handlers': ['request'],
            'propagate': True
        },
        "error": {
            'level': 'INFO',
            'handlers': ['error'],
            'propagate': True
        },
    }
}


class Config(object):
    SECRET_KEY = env.get('SECRET_KEY') or os.environ.get('SECRET_KEY') or 'simple flask website'

    LOGGING = LOGGING

    JWT_SECRET_KEY = env.get('SECRET_KEY') or os.environ.get('JWT_SECRET_KEY') or 'simple flask website'

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = '994171686@qq.com'
    MAIL_PASSWORD = 'fsiwanjpsnyrbdbc'

    MAIL_SUBJECT_PREFIX = '[simple_website]'
    MAIL_SENDER = 'Simple Website Admin <994171686@qq.com>'

    # CACHE_TYPE = 'redis'
    # CACHE_REDIS_URL = 'redis://localhost:6379/1'

    CACHE_TYPE = 'FileSystemCache'
    CACHE_DIR = "flask_cache_dir"

    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "pool_size": 5,
    #     "pool_recycle": 60 * 60 * 2,
    #     "pool_pre_ping": True,
    # }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URI') or os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    # TESTING = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URI') or os.environ.get('DEV_DATABASE_URI') or \
        'sqlite://'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
