# coding: utf-8
import uuid
import arrow


def utcnow():
    return arrow.utcnow().datetime


def get_uuid():
    return uuid.uuid4().hex
