# coding: utf-8
from logging.config import dictConfig
from flask import Flask
from flask_mail import Mail
from flask_caching import Cache
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import config


db = SQLAlchemy()
mail = Mail()
cache = Cache()
basic_auth = HTTPBasicAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    dictConfig(config[config_name].LOGGING)
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    JWTManager(app)

    from .handlers import register_handlers
    from .controllers.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    register_handlers(app)

    @app.route('/hello')
    def hello():
        return 'Hellow World!'

    return app
