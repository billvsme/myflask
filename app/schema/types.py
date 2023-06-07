# coding: utf-8
import arrow

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy.orm.query import Query
from ..models.auth import User as UserModel


class MyConnection(relay.Connection):

    class Meta:
        abstract = True

    total_count = graphene.Int(description="Total count", required=True)

    def resolve_total_count(root, info, **args):
        if isinstance(root.iterable, Query):
            _len = root.iterable.count()
        else:
            _len = len(root.iterable)

        return _len


class MySQLAlchemyObjectType(SQLAlchemyObjectType):
    create_time = graphene.String(description="创建时间", required=True)
    update_time = graphene.String(description="更新时间", required=True)

    def resolve_create_time(self, info):
        return arrow.get(self.create_time).isoformat()

    def resolve_update_time(self, info):
        return arrow.get(self.update_time).isoformat()

    def resolve_id(self, info):
        return self.uuid

    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, info, id):
        return cls.get_query(info).filter_by(uuid=id).first()


class User(MySQLAlchemyObjectType):

    class Meta:
        model = UserModel
        exclude_fields = ("password_hash",)
        description = "用户"

        interfaces = (relay.Node,)
        connection_class = MyConnection
