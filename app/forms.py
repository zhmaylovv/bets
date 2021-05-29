from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_wtf.file import FileField, FileRequired
from datetime import datetime






class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    fio = StringField('Имя по котрое будет видно пользователям', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    photo = FileField('Выберите фото', validators=[FileRequired()] )

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditUserForm(FlaskForm):

    fio = StringField('Имя по котрое будет видно пользователям')
    email = StringField('Email')
    password = PasswordField('Password')
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
    photo = FileField('Выберите фото')

    submit = SubmitField('Edit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class MatchEditForm(FlaskForm):

    team1 = StringField('Комманда 1', validators=[DataRequired()])
    team2 = StringField('Комманда 2', validators=[DataRequired()])
    t1_res = StringField('Результат Комманды 1')
    t2_res = StringField('Результат Комманды 2')
    datetime = DateTimeField('Дата и время', validators=[DataRequired()], default= datetime.utcnow())
    submit = SubmitField('Сохранить')
    delete = BooleanField( 'Удалить матч' )


class BetsEditForm(FlaskForm):

    t1_pre = StringField('Результат Комманды 1', validators=[DataRequired()], default='0')
    t2_pre = StringField('Результат Комманды 2', validators=[DataRequired()], default='0')
    comment = TextAreaField('Комментарий к матчу', validators=[Length(max=140)])

    submit = SubmitField('Сохранить')