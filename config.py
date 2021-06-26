import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    SQLALCHEMY_DATABASE_URI = os.environ.get ( 'DATABASE_URL' )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
    SECRET_KEY = os.environ.get ( 'SECRET_KEY' ) or 'slonik'
    SQLALCHEMY_DATABASE_URI = ( 'postgres://aqtwmbttymvkxz:c08f1d41e01307e8681c72f5380251858560d8f0c231d1e771234476c72f1291@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/d6a2uunt15rsls' )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''