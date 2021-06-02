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
#db.create_all()
# try:
#     user_list = User.query.order_by(User.score.desc()).all ()
# except
#     db.create_all ()
# if len(user_list) < 1:
#     admin = User(username="admin", email="14hp@ngs.ru", fio="Администратор")
#     admin.set_password("admin")
#     db.session.add ( admin )
#     db.session.commit()