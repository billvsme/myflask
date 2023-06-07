# coding: utf-8
import graphene
from graphene import relay
from graphql_relay.utils import unbase64
from .types import User
from .fields import MyConnectionField
from .filters import UserFilter


class Query(graphene.ObjectType):

    node = relay.Node.Field()

    user_list = MyConnectionField(
        User.connection, filters=UserFilter(), all=graphene.Boolean(), sort=None)

    def resolve_user_list(root, info, **kwargs):
        model = kwargs.pop("model")
        query = Query.user_list.get_query(model, info, **kwargs)
        filters = kwargs.get("filters", {})
        if "uuid" in filters:
            query = query.filter_by(uuid=filters["uuid"])
        if "id" in filters:
            uuid = unbase64(filters["id"]).split(":")[-1]
            query = query.filter_by(uuid=uuid)
        if "is_admin" in filters:
            query = query.filter_by(is_admin=filters["is_admin"])

        return query
