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
    db.create_all ()
try:
    admin = User(id=1, username="admin", email="change@email.ru", fio="Администратор")
    admin.set_password("admin")
    with open ( 'app/static/admin.jpg' ,"rb" ) as f:
        admin.avatar = f.read ()
    db.session.add ( admin )
    db.session.commit()
except:
    pass

