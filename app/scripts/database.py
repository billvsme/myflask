# coding: utf-8
import click
from sqlalchemy.sql import or_

from .. import db
from ..models.auth import User


def init_db():
    db.create_all()


@click.argument("email")
@click.argument("username")
@click.argument("password")
def create_user(email, username, password):
    user = User.query.filter(or_(User.email == email, User.username == username)).first()
    if not user:
        User.save({
            "email": email, "username": username, "password": password,
            "confirmed": True, "is_admin": True})
