import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{base_dir}/blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
