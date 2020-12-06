# coding: utf-8
from setuptools import find_packages, setup


setup(
    name='simple_website',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'itsdangerous'
        'schema'
    ]
)
