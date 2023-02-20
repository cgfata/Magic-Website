import os
import mysql.connector
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from urllib.parse import quote

# load_dotenv()
# BOT_TOKEN = os.getenv('TOKEN')
# MAGIC_INVENTORY_HOST = os.getenv('HOST')
# MAGIC_INVENTORY_USER = os.getenv('USER')
# MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
# MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')
# MAGIC_INVENTORY_PASSWORD_S = os.getenv('PASSWORD_AZURE')
# MAGIC_INVENTORY_HOST_AZURE = os.getenv('HOST_AZURE')

BOT_TOKEN = os.environ.get('TOKEN')
MAGIC_INVENTORY_HOST = os.environ.get('HOST')
MAGIC_INVENTORY_USER = os.environ.get('USER')
MAGIC_INVENTORY_PASSWORD = os.environ.get('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.environ.get('DATABASE')
MAGIC_INVENTORY_PASSWORD_S = os.environ.get('PASSWORD_AZURE')
MAGIC_INVENTORY_HOST_AZURE = os.environ.get('HOST_AZURE')

# get the directory containing the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# get the current working directory
cwd = os.getcwd()

# construct the path to the target file relative to the current working directory
file_path = os.path.join(cwd, "DigiCertGlobalRootCA.crt.pem")

# print the absolute file path
MAGIC_Inventory_SSL_CA = os.path.abspath(file_path)

# print the absolute file path
print(MAGIC_Inventory_SSL_CA)


# #password = quote(MAGIC_INVENTORY_PASSWORD_S)
# password = quote(str(MAGIC_INVENTORY_PASSWORD_S))


db = SQLAlchemy()
#DB_NAME = "mysql+pymysql://inventorybot:gio91030@localhost/testingdatabase"
#DB_NAME = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD }@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'
DB_NAME = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD_S}@{MAGIC_INVENTORY_HOST_AZURE}:3306/{MAGIC_INVENTORY_DATABASE}?ssl=true'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://inventorybot:gio91030@localhost/testingdatabase'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD }@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'
    ssl_args = {
        "ssl": {
            #"ca": "F:/Documents\Python Projects/flaskProject/DigiCertGlobalRootCA.crt.pem",
            "ca": f'{MAGIC_Inventory_SSL_CA}',
            "check_hostname": False
        }
    }
    uri = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD_S}@{MAGIC_INVENTORY_HOST_AZURE}:3306/{MAGIC_INVENTORY_DATABASE}?ssl=true'
    uri_params = {"connect_args": ssl_args}
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = uri_params
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