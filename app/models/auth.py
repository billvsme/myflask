# coding: utf-8
from datetime import timedelta

import arrow
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_jwt_extended import create_access_token, decode_token

from .. import db
from ..utils.common import get_uuid, utcnow


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), default=get_uuid, unique=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, nullable=False, default=utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    @classmethod
    def save(cls, data):
        user = cls(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            confirmed=data.get('confirmed', False),
            is_admin=data.get('is_admin', False),
        )

        db.session.add(user)
        db.session.commit()

        return user

    def to_json(self):
        return {
            "uuid": self.uuid,
            "email": self.email,
            "username": self.username,
            "confirmed": self.confirmed,
            "is_admin": self.is_admin,
            "create_time": arrow.get(self.create_time).isoformat(),
            "update_time": arrow.get(self.update_time).isoformat()
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=14*24*60*60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def generate_auth_jwt_token(self, expiration=14*24*60*60):
        return create_access_token(
            {"id": self.id},
            expires_delta=timedelta(seconds=expiration)
        )

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return None

        return User.query.get(data['id'])

    def generate_confirmation_token(self, expiration=3600):
        return create_access_token(
            {"confirm": self.id},
            expires_delta=timedelta(seconds=expiration)
        )

    def confirm(self, token):
        try:
            data = decode_token(token)
            assert data['identity']['confirm'] == self.id
        except Exception:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=60*60):
        return create_access_token(
            {"reset": self.id},
            expires_delta=timedelta(seconds=expiration)
        )

    @staticmethod
    def reset_password(token, new_password):
        user = None
        try:
            data = decode_token(token)
            user = User.query.get(data['identity']['reset'])
        except Exception:
            return False

        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
