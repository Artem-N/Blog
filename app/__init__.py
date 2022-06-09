from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


fapp = Flask(__name__)
fapp.config.from_object(Config)

db = SQLAlchemy(fapp)
migrate = Migrate(fapp, db)
login = LoginManager(fapp)

login.login_view = 'login'


from app import views, models, forms, login
