from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime

from app import db, login


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        kwargs['password'] = self.set_password(kwargs.get('password'))
        super().__init__(*args, **kwargs)

    def set_password(self, raw_password):
        return generate_password_hash(raw_password)


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship(User, backref=db.backref('posts', lazy=True))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
