# coding: utf-8
from flask import g, request, Blueprint
from schema import Schema, And, Use, Optional, SchemaError
from flasgger import swag_from
from sqlalchemy.sql import or_

from ..utils.auth import login_required
from .. import db, basic_auth
from ..email import send_email
from ..errors import bad_request, forbidden, unauthorized
from ..models.auth import User
from ..docs.auth import login_swagger, register_swagger, change_password_swagger

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('login', methods=['POST'])
@swag_from(login_swagger)
def login():
    json_data = request.get_json()

    try:
        validated = Schema({
            "username": And(Use(str), len, error='Incorrect username.'),
            'password': And(Use(str), lambda s: len(s) >= 6, error='Incorrect password.')
        }).validate(json_data)
    except SchemaError as e:
        return {'code': -1, 'error': str(e)}, 500

    user = User.query.filter(or_(
        User.username == validated['username'],
        User.email == validated['username']),
        User.confirmed.is_(True)
    ) .first()
    if not user or \
            not user.verify_password(validated['password']):
        return unauthorized('username or password error')

    EXPIRATION = 14*24*60*60
    return {
        'access_token': user.generate_auth_jwt_token(expiration=EXPIRATION),
        'expiration': EXPIRATION
    }, 200


@auth_bp.route('/register', methods=['POST'])
@swag_from(register_swagger)
def register():
    json_data = request.get_json()

    try:
        validated = Schema({
            'email': And(Use(str), len, error='Incorrect email.'),
            'username': And(Use(str), len, error='Incorrect username.'),
            'password': And(Use(str), lambda s: len(s) >= 6, error='Incorrect password.')
        }).validate(json_data)
    except SchemaError as e:
        return {'code': -1, 'error': str(e)}, 500

    user = User(email=validated['email'],
                username=validated['username'],
                password=validated['password'])
    db.session.add(user)
    db.session.commit()

    EXPIRATION = 60 * 60
    token = user.generate_confirmation_token(EXPIRATION)

    send_email(user.email, 'Confirm Your Account',
               'email/confirm', user=user, token=token)

    return {'message': 'success'}, 200


@auth_bp.route('/confirm')
@login_required
def resend_confirmation():
    EXPIRATION = 60 * 60
    token = g.current_user.generate_confirmation_token(EXPIRATION)

    send_email(g.current_user.email, 'Confirm Your Account',
               'email/confirm', user=g.current_user, token=token)

    return {'message': 'success'}, 200


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if g.current_user.confirmed:
        return bad_request('already confirmed')
    if g.current_user.confirm(token):
        db.session.commit()
    return {'message': 'success'}, 200


@auth_bp.route('/change-password', methods=['POST'])
@login_required
@swag_from(change_password_swagger)
def change_password():
    json_data = request.get_json()

    try:
        validated = Schema({
            'old_password': And(Use(str), lambda s: len(s) >= 6, error='Incorrect old_password.'),
            'new_password': And(Use(str), lambda s: len(s) >= 6, error='Incorrect new_password.')
        }).validate(json_data)
    except SchemaError as e:
        return {'code': -1, 'error': str(e)}, 500

    if not g.current_user.verify_password(validated['old_password']):
        return bad_request('Incorrect old_password')

    g.current_user.password = validated['new_password']
    db.session.add(g.current_user)
    db.session.commit()
    return {'message': 'success'}, 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_request():
    json_data = request.get_json()

    try:
        validated = Schema({
            'email': And(Use(str), lambda s: len(s) >= 6, error='Incorrect email.'),
        }).validate(json_data)
    except SchemaError as e:
        return {'code': -1, 'error': str(e)}, 500

    user = User.query.filter_by(email=validated['email']).first()
    if user:
        token = user.generate_reset_token()
        send_email(user.email, 'Reset your password',
                   'email/reset_password', user=user, token=token)

    return {'message': 'success'}, 200


@auth_bp.route('/reset-password/<token>')
def reset_password(token):
    json_data = request.get_json()

    try:
        validated = Schema({
            'new_password': And(Use(str), lambda s: len(s) >= 6, error='Incorrect new_password.')
        }).validate(json_data)
    except SchemaError as e:
        return {'code': -1, 'error': str(e)}, 500

    if not User.reset_password(token, validated['new_password']):
        return bad_request('reset password error')

    return {'message': 'success'}, 200
