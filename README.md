simple-website
==============

## run
```
development

python -m venv ./venv
. ./venv/bin/activate
pip install -e . 
(or python setup.py develop)

export FLASK_APP="simple_website.py"
export FLASK_ENV=development
flask run

curl http://127.0.0.1:5000/hello
```
