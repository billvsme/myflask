# coding: utf-8
from .common import AUTH


login_swagger = {
    "tags": ["权限"],
    "description": "登录",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                # "id": "接口参数示例2",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "用户名",
                        "example": "test"
                    },
                    "password": {
                        "type": "string",
                        "description": "密码",
                        "example": "password"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "200返回",
            "schema": {
                "example": {
                    "access_token": "token",
                    "expiration": 43200
                }
            }
        }
    }
}

register_swagger = {
    "tags": ["权限"],
    "description": "注册",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                # "id": "接口参数示例2",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "邮箱",
                        "example": "test2@qq.com"
                    },
                    "username": {
                        "type": "string",
                        "description": "用户名",
                        "example": "test2"
                    },
                    "password": {
                        "type": "string",
                        "description": "密码",
                        "example": "password"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "200返回",
            "schema": {
                "example": {
                    "access_token": "token",
                    "expiration": 43200
                }
            }
        }
    }
}

change_password_swagger = {
    "tags": ["权限"],
    "description": "修改密码",
    "parameters": [AUTH, {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                # "id": "接口参数示例2",
                "properties": {
                    "old_password": {
                        "type": "string",
                        "description": "旧密码",
                        "example": "password"
                    },
                    "new_password": {
                        "type": "string",
                        "description": "新密码",
                        "example": "password"
                    },
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "200返回",
            "schema": {
                "example": {
                    "access_token": "token",
                    "expiration": 43200
                }
            }
        }
    }
}
