# coding: utf-8
import json
import logging
import traceback

from flask import g, request
from graphql_server import default_format_error

from . import basic_auth
from .models.auth import User
from .errors import unauthorized, forbidden

request_logger = logging.getLogger('request')
error_logger = logging.getLogger('error')
graphql_error_logger = logging.getLogger('graphql_error')


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
    user_id = "geterr"
    try:
        user_id = g.current_user.id if hasattr(g, 'current_user') and g.current_user else None
    except Exception:
        pass

    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token, Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    log_message = "{},{},{},{},{},{},".format(
        request.headers.get("X-Real-Ip") or request.remote_addr,
        request.url, resp.status, user_id,
        json.dumps(request.args, ensure_ascii=False),
        request.get_data()
    )

    try:
        resp_data = json.dumps(resp.get_json(), ensure_ascii=False)[:200]
        log_message += resp_data
    except Exception:
        log_message += "{}".format(resp.data[:200])

    request_logger.info(log_message)

    if resp.status_code == 500:
        try:
            resp_data = json.dumps(resp.get_json(), ensure_ascii=False)[:1000]
            log_message += resp_data
        except Exception:
            log_message += "{}".format(resp.data[:1000])

        error_logger.info(log_message)

    return resp


def errorhandler(error):
    user_id = "geterr"
    try:
        user_id = g.current_user.id if hasattr(g, 'current_user') and g.current_user else None
    except Exception:
        pass

    log_message = "{},{},{},{},{}".format(
        request.url, user_id,
        json.dumps(request.args, ensure_ascii=False)[:1000],
        request.get_data()[:1000],
        traceback.format_exc()
    )

    error_logger.error(log_message)


def register_handlers(app):
    app.before_request(before_request)
    app.after_request(after_request)
    app.errorhandler(500)(errorhandler)


def log_and_format_exception(self, error):
    user_id = "geterr"
    try:

        user_id = g.current_user.id if hasattr(g, 'current_user') and g.current_user else None
    except Exception:
        pass

    try:
        error.reraise()
    except Exception:
        log_message = "{},{},{}".format(error.path, user_id, traceback.format_exc())
        graphql_error_logger.error(log_message)

    return default_format_error(error)
