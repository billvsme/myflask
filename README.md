myflask
==============
flask快速启动项目，包含
- 基础用户登陆注册
- Swagger文档支持
- GraphQL支持(Relay)
- 阿里云SDK
- 图片缩放服务
- .env支持

## 运行
```
开发环境

python -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 修改.env为合适的值

export FLASK_APP="myflask"
export FLASK_CONFIG=development
flask run

curl http://127.0.0.1:5000/hello
```

## Swagger
浏览器打开 http://127.0.0.1:5000/apidocs

## GraphQL
浏览器打开 http://127.0.0.1:5000/graphql  
支持Relay
```
# 用户筛选
query {
  userList(page: 1, pageSize: 2) {
    edges {
      node {
        id,
        username
      }
    }	
  }
}


# 创建用户
mutation test {
  createUser(email: "test3@qq.com", username:"test3", password: "password") {
    ok,
    code,
    message
  }
}
```

## 文件缩放服务
支持对图片缩放,通过w指定宽度  
浏览器打开 http://127.0.0.1:5000/file/image/1.jpg?w=100  

## 阿里云SDK
代码路径 app/utils/aliyun.py  
目前包含短信发送  

## 正式环境部署
```
supervisor配置参考supervisor/myflask.conf.example
```
