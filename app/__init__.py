import time

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
from app.models import User

try:
    user_list = User.query.all()
except:
    print ("create")
    db.create_all()
    db.session.commit()
    time.sleep(3)
    print("if")
    admin = User(id=1, username="admin", email="change@email.ru", fio="Администратор")
    admin.set_password("admin")
    with open('app/static/admin.jpg', "rb") as f:
        admin.avatar = f.read()
    db.session.add(admin)
    db.session.commit()
'''
admin
pbkdf2:sha256:150000$h3TBJoLF$86a5d41268301815f3d6a35e7cdf251c0fc01c3074ae7f3f090d241f3cde95a4
'''