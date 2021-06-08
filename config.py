import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    SQLALCHEMY_DATABASE_URI = os.environ.get ( 'DATABASE_URL' )
    SQLALCHEMY_TRACK_MODIFICATIONS = False