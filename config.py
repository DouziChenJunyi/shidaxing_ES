#encoding: utf-8
import os
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'Chenjunyi1998.'
HOST = '127.0.0.1'
PORT = '3306'
# DATABASE = 'mysql_for_shidaxing'
DATABASE = 'sys'
SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

ARTISAN_POSTS_PER_PAGE = 3

basedir = os.path.abspath(os.path.dirname(__file__))
PATH_BEFORE = basedir + '/static/images/'
