import os
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Match, Bets
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, MatchEditForm, BetsEditForm, EditUserForm
from werkzeug.utils import secure_filename
from datetime import datetime
from app.func import result_calc, set_auto_bet, score_for_users_calc


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

@app.route('/')
@app.route('/bets')
@login_required
def bets():

    user_list = User.query.all()
    match_list = Match.query.all()
    bets_dict = {}
    res_dict = {}
    count = 0

    all_matchs = Match.query.all ()
    all_users = User.query.order_by(User.score.desc()).all ()
    main_table_dict = {}
    # main_table_dict = {"match": {team1: name, team2:name, t1_res: n, t2_res: n, users: {name: name, t1_pre: , t2_pre, score},} }
    for match in all_matchs:
        match_name = "matchs" + str ( match.id )
        main_table_dict[match_name] = {}
        main_table_dict[match_name]["team1"] = match.team1
        main_table_dict[match_name]["team2"] = match.team2
        main_table_dict[match_name]["t1_res"] = match.t1_res
        main_table_dict[match_name]["t2_res"] = match.t2_res
        main_table_dict[match_name]["users"] = {}
        for user in all_users:
            main_table_dict[match_name]["users"][user.id] = {}
            bet_to_dict = Bets.query.filter_by ( match_id=match.id ,user_id=user.id ).first()
            if bet_to_dict:
                main_table_dict[match_name]["users"][user.id]["fio"] = user.fio
                main_table_dict[match_name]["users"][user.id]["t1_pre"] = bet_to_dict.t1_pre
                main_table_dict[match_name]["users"][user.id]["t2_pre"] = bet_to_dict.t2_pre
                main_table_dict[match_name]["users"][user.id]["scor"] = bet_to_dict.res_scor


    for user in user_list:
        user_id = user.id
        user_bets = Bets.query.filter_by(user_id=user_id).all()
        bets_dict[user.username] = {}

        for bet in user_bets:
            match = Match.query.filter_by(id=bet.match_id).first_or_404()
            data = {"match.team1": match.team1 ,"match.team2": match.team2 ,"bet.t1_pre": bet.t1_pre ,
                    "bet.t2_pre": bet.t2_pre ,
                    "match.t1_res": match.t1_res ,"match.t2_res": match.t2_res ,"bet.comment": bet.comment}
            if match.completed:
                res_dict[bet.res_scor] = [str(match.team1) + "-" + str(match.team2) + " ставка: " \
                                     + str(bet.t1_pre) + "-" + str(bet.t2_pre) + " результат: " \
                                     + str(match.t1_res) + "-" + str(match.t2_res) + " | " + str(bet.comment), data]
                bets_dict[user.username][match.id] = res_dict

            res_dict = {}

    return render_template( 'bets.html' , bets_dict= bets_dict, main_table_dict = main_table_dict, all_users = all_users )

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

@app.route('/edituser/<username>', methods=['GET', 'POST'])
@login_required
def edituser(username):
    form = EditUserForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}]
    avatar = User.avatar

    if form.validate_on_submit():
        if form.password.data:
            user.set_password=form.password.data
        if form.email.data:
            user.email=form.email.data
        if form.fio.data:
            user.fio=form.fio.data
        if form.photo.data:
            f = form.photo.data
            filename = secure_filename(f.filename)
            if form.photo.data.content_type.split('/')[0] != 'image':
                flash('Image only plz')
                return redirect(url_for('edituser'))
            f.save(os.path.join(os.getcwd() + '/venv/app/static', username + '.' + filename.split('.')[-1]))
            user.avatar = (username + '.' + filename.split('.')[-1])
        db.session.commit()
        flash('Edit ok')

        return redirect(url_for('index'))
    return render_template('edituser.html', user=user, posts=posts, avatar= avatar, form=form)

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
    '''if current_user.username != 'admin':
        return redirect(url_for('matchs'))
    form = MatchEditForm()
    if form.validate_on_submit():'''
    if request.method == 'POST':

        match = Match(team1=request.form.get('team1'), team2=request.form.get('team2'), timestamp=request.form.get('datatime'), t1_res='',
                      t2_res='',)
        db.session.add(match)
        db.session.commit()

        #добавили матч, нужно добавить всем ставки - 0-0

        flash('Матч добавлен')
        return redirect(url_for('matchs'))

    return render_template('matchadd.html') #form=form


@app.route('/matchs', methods=['GET', 'POST'])
@login_required
def matchs():
    matchs = Match.query.all()
    bets = Bets.query.filter_by(user_id=current_user.id).all()
    return render_template('matchs.html', matchs=matchs, bets=bets)

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
            if form.t2_res.data != '' and form.t1_res.data != '': #вот такая кривенькая проверка на заполненность полей
                try:
                    edit.t2_res = int(form.t2_res.data)
                    edit.t1_res = int(form.t1_res.data)
                except ValueError:
                    flash ( 'Результаты матча заполнены не корректно!' )
                    return render_template ( 'editmatch.html' ,form=form ,edit=edit )
                if edit.t2_res >= 0  and edit.t2_res >= 0:
                    edit.completed = True
            else:
                edit.t2_res = form.t2_res.data
                edit.t1_res = form.t1_res.data
                edit.completed = False
            edit.timestamp = form.datetime.data
            db.session.commit()
            if edit.completed:

                set_auto_bet (match_id)
                result_calc(match_id)
                score_for_users_calc()
                pass
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
    if datetime.utcnow () < match.timestamp and not match.completed:

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
    flash ( 'Ставки сделаны, ставок больше нет... на этот матч!' )
    return redirect ( url_for ( 'matchs' ) )