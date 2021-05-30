import os
import MySQLdb


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    SQLALCHEMY_DATABASE_URI = "mysql://u1355337_admin:vA6tF4oX1neX5g@31.31.196.189:3306/u1355337_bets"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    # SQLALCHEMY_DATABASE_URI = os.environ.get ( 'DATABASE_URL' ) or \
    #                           'sqlite:///' + os.path.join ( basedir ,'bets.db' )
    # SQLALCHEMY_TRACK_MODIFICATIONS = False