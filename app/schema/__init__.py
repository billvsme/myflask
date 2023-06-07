# coding: utf-8
import graphene
from graphene_sqlalchemy.converter import convert_sqlalchemy_type

from .. import db
from .query import Query
from .mutation import Mutation


@convert_sqlalchemy_type.register(db.DateTime)
def convert_column_to_datetime(type, column, registry=None):
    return graphene.String


schema = graphene.Schema(query=Query, mutation=Mutation)
