# coding: utf-8
import graphene


class UserFilter(graphene.InputObjectType):
    id = graphene.String()
    uuid = graphene.String()
    is_admin = graphene.Boolean()
