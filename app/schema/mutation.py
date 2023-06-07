# coding: utf-8
import graphene
from schema import Schema, And, Use, SchemaError, Optional
from sqlalchemy.sql import or_

from .. import db
from ..models.auth import User


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    code = graphene.Int()
    message = graphene.String()

    def mutate(root, info, **kwargs):
        try:
            validated = Schema({
                "email": And(Use(str), len, error='机构名称不合法'),
                "username": And(Use(str), len, error='机构简称不合法'),
                "password": And(Use(str), len, error='机构编号不合法'),
            }).validate(kwargs)
        except SchemaError as e:
            return CreateUserMutation(ok=False, code=-1, message=str(e))

        user = User.query.filter(or_(
            User.email == validated["username"], User.username == validated["username"])).first()
        if user:
            return CreateUserMutation(ok=False, code=-1, message="用户已存在")

        User.save({**validated})

        return CreateUserMutation(ok=True, code=0, message="success")


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
