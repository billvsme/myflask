simple-website
==============

## 运行
```
development

python -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 修改.env为合适的值

export FLASK_APP="simple_website.py"
export FLASK_ENV=development
flask run

curl http://127.0.0.1:5000/hello
```

## Swagger
浏览器打开 http://127.0.0.1:5000/apidocs

## graphql
浏览器打开 http://127.0.0.1:5000/graphql
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
