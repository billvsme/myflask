# coding: utf-8
from functools import partial
from promise import Promise, is_thenable

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy.fields import registerConnectionFieldFactory
from flask import current_app
from sqlalchemy.orm.query import Query
from graphql_relay.connection.arrayconnection import offset_to_cursor
from graphql_relay.connection.arrayconnection import connection_from_list_slice
from graphene.relay.connection import PageInfo


class PageSQLAlchemyConnectionField(SQLAlchemyConnectionField):
    def __init__(self, type, *args, **kwargs):
        kwargs["page"] = graphene.Int()
        kwargs["page_size"] = graphene.Int()
        super(PageSQLAlchemyConnectionField, self).__init__(type, *args, **kwargs)

    @classmethod
    def resolve_connection(cls, connection_type, model, info, args, resolved):
        if resolved is None:
            resolved = cls.get_query(model, info, **args)
        if isinstance(resolved, Query):
            _len = resolved.count()
        else:
            _len = len(resolved)

        offset = 0
        if "page" in args:
            page_size = int(args.get('page_size', current_app.config['PAGE_SIZE']))
            page = int(args.get('page'))

            offset = (page - 1) * page_size
            limit = page_size

            args["first"] = limit
            args["after"] = offset_to_cursor(offset-1)

        if "all" in args and args["all"]:
            args["first"] = _len
            args["after"] = offset_to_cursor(-1)

        connection = connection_from_list_slice(
            resolved,
            args,
            slice_start=0,
            list_length=_len,
            list_slice_length=_len,
            connection_type=connection_type,
            pageinfo_type=PageInfo,
            edge_type=connection_type.Edge,
        )
        connection.iterable = resolved
        connection.length = _len
        return connection

    @classmethod
    def connection_resolver(cls, resolver, connection_type, model, root, info, **kwargs):
        kwargs["connection_type"] = connection_type
        kwargs["model"] = model
        resolved = resolver(root, info, **kwargs)

        on_resolve = partial(cls.resolve_connection, connection_type, model, info, kwargs)
        if is_thenable(resolved):
            return Promise.resolve(resolved).then(on_resolve)

        return on_resolve(resolved)


# class MyFilterableConnectionField(FilterableConnectionField):
#     pass


class MyConnectionField(PageSQLAlchemyConnectionField):
    def __init__(self, type, *args, **kwargs):
        # kwargs["id"] = graphene.String()
        # kwargs["uuid"] = graphene.String()
        super(MyConnectionField, self).__init__(type, *args, **kwargs)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        return super(MyConnectionField, cls).get_query(model, info, sort, **args)


registerConnectionFieldFactory(MyConnectionField)
