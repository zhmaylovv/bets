import os
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Match, Bets
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, MatchEditForm, BetsEditForm
from werkzeug.utils import secure_filename
from datetime import datetime




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name= 'FLAAAASK')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/bets')
@login_required
def bets():

    return render_template('bets.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, fio=form.fio.data)
        user.set_password(form.password.data)
        f = form.photo.data
        filename = secure_filename(f.filename)
        print(f.content_type)
        if form.photo.data.content_type.split('/')[0] != 'image':
            flash('Image only plz')
            return redirect(url_for('register'))


        f.save(os.path.join(os.getcwd() + '/venv/app/static',  form.username.data + '.' + filename.split('.')[-1]))
        user.avatar = (form.username.data + '.' + filename.split('.')[-1])
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Please log in')

        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    avatar = User.avatar
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts, avatar= avatar)


@app.route('/matchadd', methods=['GET', 'POST'])
@login_required
def matchadd():
    if current_user.username != 'admin':
        return redirect(url_for('matchs'))
    form = MatchEditForm()
    if form.validate_on_submit():
        match = Match(team1=form.team1.data, team2=form.team2.data, t1_res= form.t1_res.data,
                      t2_res=form.t2_res.data, timestamp=form.datetime.data)
        db.session.add(match)
        db.session.commit()
        flash('Матч добавлен')
        return redirect(url_for('matchs'))

    return render_template('matchadd.html', form=form)

@app.route('/matchs', methods=['GET', 'POST'])
def matchs():
    matchs = Match.query.all()
    return render_template('matchs.html', matchs= matchs)

@app.route('/editmatchs/<match_id>', methods=['GET', 'POST'])
@login_required
def editmatchs(match_id):

    if current_user.username == 'admin':
        edit = Match.query.filter_by(id=match_id).first_or_404()
        form = MatchEditForm()

        if form.validate_on_submit():
            '''match = Match(id= match_id, team1=form.team1.data, team2=form.team2.data, t1_res=form.t1_res.data,
                          t2_res=form.t2_res.data, timestamp=form.datetime.data)'''
            edit.team1 = form.team1.data
            edit.team2 = form.team2.data
            edit.t2_res = form.t2_res.data
            edit.t1_res = form.t1_res.data
            edit.timestamp = form.datetime.data
            edit.completed = form.completed.data
            print (form.completed.data)
            ''' 
            Вставить сюда код обработки завершенного матча...
            
            '''


            db.session.commit()
            return redirect(url_for('matchs'))
        return render_template('editmatch.html', form=form, edit=edit)
    else:
        return redirect(url_for('matchs'))
    return redirect(url_for('matchs'))

@app.route('/editbets/<match_id>', methods=['GET', 'POST'])
@login_required
def editbets(match_id):
    form = BetsEditForm()
    match = Match.query.filter_by(id=match_id).first_or_404()
    users = User.query.all()
    all_bet = Bets.query.filter_by(match_id=match_id).all()
    my_bet = Bets.query.filter_by(match_id=match_id, user_id=current_user.id).first()

    udic = {}
    for i in users:
        udic[i.id] = i.fio

    if form.validate_on_submit():
        if my_bet is None:
            my_bet = Bets(match_id= match_id, user_id= current_user.id, t1_pre=form.t1_pre.data, t2_pre=form.t2_pre.data,
                          comment=form.comment.data)
            print(my_bet.match_id)
            db.session.add(my_bet)
            db.session.commit()

        else:
            my_bet.match_id = match_id
            my_bet.user_id = current_user.id
            my_bet.t1_pre = form.t1_pre.data
            my_bet.t2_pre = form.t2_pre.data
            my_bet.comment = form.comment.data
            db.session.commit()
        return redirect(url_for('matchs'))



    return render_template('editbets.html', form=form, match=match, all_bet=all_bet, my_bet=my_bet, udic= udic)

