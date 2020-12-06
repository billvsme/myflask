# coding: utf-8
from flask import g, request

from . import basic_auth
from .models.auth import User
from .errors import unauthorized, forbidden
from .controllers.auth import auth_bp


@basic_auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.get_current_user(email_or_token)
        g.token_userd = True
        return g.current_user is not None

    user = User.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False

    g.current_user = user
    g.token_userd = False
    return user.verify_passwordpass(password)


@basic_auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@auth_bp.before_app_request
def before_request():
    if hasattr(g, 'current_user') \
            and not g.current_user.confirmed:
        return forbidden('Unconfirm account')

@auth_bp.after_app_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return resp
