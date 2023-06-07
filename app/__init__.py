# coding: utf-8
from logging.config import dictConfig
from flask import Flask
from flask_mail import Mail
from flask_caching import Cache
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_graphql import GraphQLView
from flasgger import Swagger
from app.utils.aliyun import Aliyun

from config import config


db = SQLAlchemy()
mail = Mail()
cache = Cache()
basic_auth = HTTPBasicAuth()
aliyun = Aliyun()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    dictConfig(config[config_name].LOGGING)
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    JWTManager(app)
    aliyun.init_app(app)

    from .handlers import register_handlers, log_and_format_exception
    from .controllers.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    register_handlers(app)

    from .scripts.database import init_db
    from .scripts.database import create_user
    app.cli.command("init_db")(init_db)
    app.cli.command("create_user")(create_user)

    # Swagger
    swagger_config = {
        "description": "myflask 接口文档",
        "title": 'myflask',
        "version": "0.1.0",
        'uiversion': 3,
        "doc_expansion": True,
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/apidocs/",

    }

    if config_name in ['testing', 'development', 'local']:
        Swagger(app, config=swagger_config)

    # GraphQL
    from .schema import schema
    from .utils.auth import admin_required

    GraphQLView.format_error = log_and_format_exception

    view = GraphQLView.as_view(
        'graphql', schema=schema,
        graphiql=True if config_name in ["local", "development", "testing"] else False
    )
    if config_name not in ["local", "development", "testing"]:
        view = admin_required(view)

    app.add_url_rule('/graphql', view_func=view)

    batch_view = GraphQLView.as_view(
        'graphql_batch', schema=schema, batch=True
    )
    if config_name not in ["local", "development", "testing"]:
        batch_view = admin_required(batch_view)
    app.add_url_rule('/graphql/batch', view_func=batch_view)

    @app.route('/hello')
    def hello():
        return 'Hellow World!'

    return app
