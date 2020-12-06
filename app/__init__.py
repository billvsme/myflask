# coding: utf-8
from flask import Flask
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()
mail = Mail()
basic_auth = HTTPBasicAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)

    from . import handlers
    from .controllers.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/hello')
    def hello():
        return 'Hellow World!'

    return app
