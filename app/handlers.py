# coding: utf-8
import traceback
import logging

from flask import g, request

from . import basic_auth
from .models.auth import User
from .errors import unauthorized, forbidden

request_logger = logging.getLogger('request')

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


def before_request():
    if hasattr(g, 'current_user') \
            and not g.current_user.confirmed:
        return forbidden('Unconfirm account')

def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    request_logger.info(
        "{},{},{},{},{}".format(
            request.url, resp.status, dict(request.args), request.get_json(), resp.data[:200]
        )
    )
    return resp

def errorhandler(error):
    request_logger.error(traceback.format_exc())

def register_handlers(app):
    app.before_request(before_request)
    app.after_request(after_request)
    app.errorhandler(500)(errorhandler)
