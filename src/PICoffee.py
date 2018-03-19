# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from views import *

if __name__ == '__main__':
  app.run(port=54321,host="0.0.0.0")
