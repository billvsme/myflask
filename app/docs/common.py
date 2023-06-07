# coding: utf-8
TOKEN = "test token"

AUTH = {
    "name": "Authorization",
    "in": "header",
    "required": True,
    "default": "Bearer " + TOKEN
}

RESP_200_OK = {
    "description": "正确返回",
    "schema": {
        "example": {"msg": "success"}
    }
}

RESP_200_ERROR = {
    "description": "错误返回",
    "schema": {
        "example": {"code": -1, "msg": "error message"}
    }
}
