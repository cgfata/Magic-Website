import os
import mysql.connector
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')


db = SQLAlchemy()
#DB_NAME = "mysql+pymysql://inventorybot:gio91030@localhost/testingdatabase"
DB_NAME = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD }@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://inventorybot:gio91030@localhost/testingdatabase'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD }@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'
    #app.config['MYSQL_USER'] = MAGIC_INVENTORY_USER
    #app.config['MYSQL_PASSWORD'] = MAGIC_INVENTORY_PASSWORD
    #app.config['MYSQL_HOST'] = MAGIC_INVENTORY_HOST
    #app.config['MYSQL_DB'] = MAGIC_INVENTORY_DATABASE
    #mysql = MySQL(app)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Inventory

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')