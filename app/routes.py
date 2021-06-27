# -*- coding: utf-8 -*-
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
from datetime import datetime, timedelta
from app.func import result_calc, set_auto_bet, score_for_users_calc
import base64
from collections import Counter




@app.route('/index')
def index():
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    return render_template('index.html', avatar= avatar)


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
    return redirect(url_for('login'))

@app.route('/')
@app.route('/bets')
@login_required
def bets():
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    user_list = User.query.order_by(User.score.desc()).all ()
    match_list = Match.query.order_by(Match.timestamp).all ()

    bets_dict = {}
    res_dict = {}

    for user in user_list:
        user.avastr =  base64.b64encode ( user.avatar ).decode ( 'ascii' )
    all_matchs = match_list
    main_table_dict = {}
    counter_list = []

    plus_15_min_time = datetime.utcnow() + timedelta(hours=4)
    for match in match_list:
        if plus_15_min_time > match.timestamp:
            match.completed = True
            set_auto_bet ( match.id )
    today_date = ( plus_15_min_time.strftime("%d.%m.%Y"))


    all_matchs =  match_list
    all_users = user_list
    # main_table_dict = {"match": {team1: name, team2:name, t1_res: n, t2_res: n, users: {name: name, t1_pre: , t2_pre, score},} }

    data_var = 0
    var_count = 1
    for match in match_list:
        counter_list.append(match.timestamp.strftime("%d.%m.%Y"))
    date_table = Counter(counter_list)
    bets_list = Bets.query.order_by ( Bets.match_id ).all ()
    pof_dict={}

    for match in all_matchs:

        match_name = "matchs" + str ( match.id )
        main_table_dict[match_name] = {}
        if plus_15_min_time.strftime("%d.%m.%Y") == match.timestamp.strftime("%d.%m.%Y"):
            main_table_dict[match_name]["today"] = True
        else:
            main_table_dict[match_name]["today"] = False
        main_table_dict[match_name]["team1"] = match.team1
        main_table_dict[match_name]["team2"] = match.team2
        if match.completed:
            main_table_dict[match_name]["t1_res"] = match.t1_res
            main_table_dict[match_name]["t2_res"] = match.t2_res
        main_table_dict[match_name]["users"] = {}
        for user in all_users:
            main_table_dict[match_name]["users"][user.id] = {}
            #bet_to_dict = Bets.query.filter_by ( match_id=match.id, user_id=user.id ).first()
            #bet_to_dict = {}
            for bet_to_dict in bets_list:
                if bet_to_dict.match_id == match.id and bet_to_dict.user_id == user.id:
                    main_table_dict[match_name]["users"][user.id]["t1_pre"] = "CHECK"
                    main_table_dict[match_name]["users"][user.id]["t2_pre"] = "CHECK"
                    if match.completed or user == current_user:
                        main_table_dict[match_name]["users"][user.id]["fio"] = user.fio
                        main_table_dict[match_name]["users"][user.id]["t1_pre"] = bet_to_dict.t1_pre
                        main_table_dict[match_name]["users"][user.id]["t2_pre"] = bet_to_dict.t2_pre
                        main_table_dict[match_name]["users"][user.id]["comment"] = bet_to_dict.comment
                        if bet_to_dict.res_scor != None:
                            main_table_dict[match_name]["users"][user.id]["scor"] = bet_to_dict.res_scor
                        else:
                            main_table_dict[match_name]["users"][user.id]["scor"] = "Игра!"
                            main_table_dict[match_name]["t1_res"] = ""
                            main_table_dict[match_name]["t2_res"] = ""

                        if match.team1.endswith('.'):

                            try:
                                if bet_to_dict.res_scor != None:
                                    pof_dict[user.id] += bet_to_dict.res_scor

                            except:
                                if bet_to_dict.res_scor != None:
                                    pof_dict[user.id] = bet_to_dict.res_scor




                if match.completed == False and user == current_user:
                    main_table_dict[match_name]["users"][user.id]["scor"] = "LINK"
                    main_table_dict[match_name]["users"][user.id]["match_id"] = match.id





    return render_template( 'bets.html' ,  main_table_dict = main_table_dict,
                            all_users = all_users,  avatar=avatar, date_table=date_table, today_date=today_date, pof_dict=pof_dict)

@login_required
@app.route('/register', methods=['GET', 'POST'])
def register():
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    # Убрал что бы залогенный админ мог видеть
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    if current_user.username == 'admin':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, fio=form.fio.data)
            user.set_password(form.password.data)
            f = form.photo.data
            try:
                if form.photo.data.content_type.split('/')[0] != 'image':
                    flash('Image only plz')
                user.avatar = f.stream.read ()
            except:
                with open ('app/static/avadefalt.jpeg' ,"rb" ) as f:
                    user.avatar = f.read()
            db.session.add(user)
            db.session.commit()
            for match in Match.query.all():
                if match.completed:
                    set_auto_bet(match.id)
                    result_calc(match.id)
            score_for_users_calc()

            flash('Congratulations, user added! Give him account info!')

            return redirect(url_for('index'))
        return render_template('register.html', title='Register', form=form, avatar=avatar)

@app.route('/edituser/<username>', methods=['GET', 'POST'])
@login_required
def edituser(username):

    form = EditUserForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}]
    avatar = base64.b64encode ( user.avatar ).decode ( 'ascii' )

    if form.validate_on_submit():
        if form.password.data:
            user.set_password(form.password.data)
        if form.email.data:
            user.email=form.email.data
        if form.fio.data:
            user.fio=form.fio.data
        if form.photo.data:
            f = form.photo.data
            if form.photo.data.content_type.split('/')[0] != 'image' and form.photo.data.content_length > 1024:

                flash('Small image only plz')
                return redirect(url_for('edituser'))

            user.avatar = f.stream.read()
        db.session.commit()
        flash('Edit ok')
        return redirect(url_for('index'))
    return render_template('edituser.html', user=user, posts=posts, avatar= avatar, form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    user = User.query.filter_by(username=username).first_or_404()
    userpic = base64.b64encode(user.avatar).decode('ascii')
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts, avatar= avatar, userpic=userpic)


@app.route('/matchadd', methods=['GET', 'POST'])
@login_required
def matchadd():
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    '''if current_user.username != 'admin':
        return redirect(url_for('matchs'))
    form = MatchEditForm()
    if form.validate_on_submit():'''
    if request.method == 'POST':

        match = Match(team1=request.form.get('team1'), team2=request.form.get('team2'), timestamp=request.form.get('datetime'), t1_res=0,
                      t2_res=0)
        db.session.add(match)
        db.session.commit()
        flash('Матч добавлен')
        return redirect(url_for('matchs'))

    return render_template('matchadd.html', avatar=avatar) #form=form


@app.route('/matchs', methods=['GET', 'POST'])
@login_required
def matchs():
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    matchs = Match.query.order_by(Match.timestamp).all ()
    bets = Bets.query.filter_by(user_id=current_user.id).all()
    return render_template('matchs.html', matchs=matchs, bets=bets, avatar=avatar)

@app.route('/editmatchs/<match_id>', methods=['GET', 'POST'])
@login_required
def editmatchs(match_id):
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    if current_user.username == 'admin':
        edit = Match.query.filter_by(id=match_id).first_or_404()
        form = MatchEditForm()
        if form.validate_on_submit():
            '''match = Match(id= match_id, team1=form.team1.data, team2=form.team2.data, t1_res=form.t1_res.data,
                          t2_res=form.t2_res.data, timestamp=form.datetime.data)'''
            if form.delete.data:
                db.session.delete ( edit )
                db.session.commit ()
                score_for_users_calc ()
                return redirect ( url_for ( 'matchs' ) )

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
                edit.t2_res = 0
                edit.t1_res = 0
                edit.completed = False
            edit.timestamp = form.datetime.data
            db.session.commit()
            if edit.completed:

                set_auto_bet (match_id)
                result_calc(match_id)
                score_for_users_calc()
                pass
            flash ( 'Матч изменен' )
            return redirect(url_for('matchs'))
        return render_template('editmatch.html', form=form, edit=edit, avatar=avatar)
    else:
        return redirect(url_for('matchs'))
    return redirect(url_for('matchs'))

@app.route('/editbets/<match_id>', methods=['GET', 'POST'])
@login_required
def editbets(match_id):
    avatar = base64.b64encode ( current_user.avatar ).decode ( 'ascii' )
    form = BetsEditForm()
    match = Match.query.filter_by(id=match_id).first_or_404()
    if datetime.utcnow() + timedelta(hours=3) < match.timestamp and not match.completed:

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
            flash ( 'Ставка сохранена!' )
            return redirect(url_for('matchs'))



        return render_template('editbets.html', form=form, match=match, all_bet=all_bet, my_bet=my_bet, udic= udic, avatar=avatar)
    flash ( 'Ставки сделаны, ставок больше нет... на этот матч!' )
    return redirect ( url_for ( 'matchs' ) )


@app.route('/bets2')
def bets2():
    user_list = User.query.order_by(User.score.desc()).all ()
    match_list = Match.query.all()

    bets_dict = {}
    res_dict = {}

    for user in user_list:
        user.avastr =  base64.b64encode ( user.avatar ).decode ( 'ascii' )
    all_matchs = match_list
    main_table_dict = {}
    counter_list = []

    plus_15_min_time = datetime.utcnow() + timedelta(minutes=15) + timedelta(hours=3)
    for match in match_list:
        if plus_15_min_time > match.timestamp:
            match.completed = True
            set_auto_bet ( match.id )

    all_matchs =  match_list
    all_users = user_list

    data_var = 0
    var_count = 1
    for match in match_list:
        counter_list.append(match.timestamp.strftime("%d.%m.%Y"))
    date_table = Counter(counter_list)
    bets_list = Bets.query.order_by ( Bets.match_id ).all ()

    for user in all_users:
        user_id = user.id
        #user_bets = Bets.query.filter_by(user_id=user_id).order_by(Bets.match_id).all()
        user_bets = []
        for bet in bets_list:
            if bet.user_id == user.id:
                user_bets.append(bet)
        bets_dict[user.fio] = {}

        for bet in user_bets:
            match_s = None
            for match in match_list:
                if match.id == bet.match_id:
                    match_s = match
                    break

            #match_s = Match.query.filter_by(id=bet.match_id).first_or_404()
            data = {"match.team1": match_s.team1 ,"match.team2": match_s.team2 ,"bet.t1_pre": bet.t1_pre ,
                    "bet.t2_pre": bet.t2_pre ,
                    "match.t1_res": match_s.t1_res ,"match.t2_res": match_s.t2_res ,"bet.comment": bet.comment, "data" : match_s.timestamp}
            if match_s.completed:
                if bet.res_scor == None:
                    res_dict[u"\u26BD"] = [str ( match_s.team1 ) + "-" + str ( match_s.team2 ) + " ставка: " \
                                              + str ( bet.t1_pre ) + "-" + str ( bet.t2_pre ) + " результат: " \
                                              + str ( match_s.t1_res ) + "-" + str ( match_s.t2_res ) + " | " + str (
                        bet.comment ) ,data]
                    bets_dict[user.fio][match_s.id] = res_dict
                else:
                    res_dict[bet.res_scor] = [str(match_s.team1) + "-" + str(match_s.team2) + " ставка: " \
                                         + str(bet.t1_pre) + "-" + str(bet.t2_pre) + " результат: " \
                                         + str(match_s.t1_res) + "-" + str(match_s.t2_res) + " | " + str(bet.comment), data]
                    bets_dict[user.fio][match_s.id] = res_dict

            res_dict = {}

    return render_template( 'bets2.html' , bets_dict= bets_dict, all_users = all_users, date_table = date_table)

@app.route('/user/list')
@login_required
def user_list():
    user_list = User.query.all ()
    user_dict = {}
    for user in user_list:
        user_dict[user.id] = user.username
    return user_dict

@app.route('/user/del/<user_id>')
@login_required
def user_del(user_id):
    if current_user.username == 'admin' and user_id != 1:
        user = User.query.filter_by( id=user_id ).first ()
        db.session.delete ( user )
        db.session.commit ()
        return "Пользователь удален"
