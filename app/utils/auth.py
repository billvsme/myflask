# coding: utf-8
from functools import wraps

from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from ..models.auth import User


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        g.current_user = None
        data = get_jwt_identity()
        if data is not None and 'id' in data:
            g.current_user = User.query.get(data['id'])

        if not g.current_user or not g.current_user.confirmed:
            return {"code": -1, "msg": "error user"}, 403

        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        g.current_user = None
        data = get_jwt_identity()
        if data is not None and 'id' in data:
            g.current_user = User.query.get(data['id'])

        if not g.current_user or not g.current_user.confirmed or not g.current_user.is_admin:
            return {"code": -1, "msg": "error user"}, 403

        return fn(*args, **kwargs)

    return wrapper
