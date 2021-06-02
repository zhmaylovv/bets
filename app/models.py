from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
'''
flask db migrate -m "users table"
flask db upgrade
'''

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pred = db.relationship('Bets', backref='author', lazy='dynamic')
    avatar = db.Column(db.LargeBinary)
    about_me = db.Column(db.String(140))
    fio = db.Column(db.String(140))
    score = db.Column(db.Integer)
    avastr = str()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)



class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(64))
    team2 = db.Column(db.String(64))
    t1_res =  db.Column(db.Integer)
    t2_res = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    bets = relationship (
        "Bets" ,
        backref="match" ,
        cascade="all, delete")

    def __repr__(self):
        return '<Match {}>'.format(self.id, self.team1, self.team2, self.t1_res, self.t2_res, self.timestamp)

class Bets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #user_fio = db.Column(db.String, db.ForeignKey('user.fio'))
    t1_pre = db.Column(db.Integer, default=0)
    t2_pre = db.Column(db.Integer, default=0)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    res_scor = db.Column(db.Integer)
    # match = relationship ( "Match" ,back_populates="bets" )

    def __repr__(self):
        return '<Bets {}>'.format(self.id, self.match_id, self.user_id, self.t1_pre, self.t2_pre, self.comment, self.timestamp, self.res_scor)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))