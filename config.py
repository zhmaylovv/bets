import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    #SQLALCHEMY_DATABASE_URI = "mysql://u1355337_admin:vA6tF4oX1neX5g@31.31.196.189:3306/u1355337_bets"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    # SQLALCHEMY_DATABASE_URI = os.environ.get ( 'DATABASE_URL' ) or \
    #                           'sqlite:///' + os.path.join ( basedir ,'bets.db' )
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES = {
        'user': 'uyrgxyycveriot' ,
        'pw': '199c91ab798dd97d8cf6d05425423e6ba3e87ffb108445bf43e252951d15f597' ,
        'db': 'dai11i8vman5e' ,
        'host': 'ec2-34-250-16-127.eu-west-1.compute.amazonaws.com' ,
        'port': '5432' ,
    }

    SQLALCHEMY_DATABASE_URI = 'postgres://uyrgxyycveriot:199c91ab798dd97d8cf6d05425423e6ba3e87ffb108445bf43e252951d15f597@ec2-34-250-16-127.eu-west-1.compute.amazonaws.com:5432/dai11i8vman5e'
    SQLALCHEMY_TRACK_MODIFICATIONS = False