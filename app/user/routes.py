from flask import render_template, Blueprint, redirect, url_for, flash, request, session, current_app as app
from app.user.forms import SignUpForm,AccountForm,LoginForm
from app.main.forms import set_evlist
from app.models import users, registrations, payments, events
from flask_login import login_required,current_user, logout_user, login_user

user = Blueprint('user', __name__)
from app import db, bcrypt

@user.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        auth_code = form.auth_code.data;
        if (auth_code == app.config['AUTH_CODE']):
            user = users(username=form.username.data,
                        name=form.name.data,
                        email=form.email.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('user.login'))
        else:
            flash('Invalid Authentication Code !  Contact Technical Secretaries or Developers.')
    else:
        print(form.errors)
    return render_template('signup.html', title='Sign Up', form=form)

@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user = users.query.filter_by(username=current_user.username).first()
    form = AccountForm(obj=user)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.old_password.data):
            user.email = form.email.data
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            if bcrypt.check_password_hash(user.password, form.new_password.data):
                flash('New Password cannot be same as Old Password')
            else:
                user.password = hashed_password
                db.session.commit()
                flash('Your account has been updated!')
        else:
            flash('Invalid password entered')
    else:
        print(form.errors)
    return render_template('account.html', title='Account', form=form)

@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #flash('Login Successful.')
            return redirect(next_page) if next_page else redirect(url_for('main.register'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    else:
        print(form.errors)
    return render_template('login.html', title='Login', form=form)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for('user.login'))

class event_list:
    def __init__(self):
        self.evlist = db.session.query(events.event_id, events.event_name, events.amt, events.solo, events.duo, events.squad, events.team, events.team_participants).order_by(events.event_id).all()
    def __repr__(self):
        return f"{self.evlist}"

@user.route('/list/<table>')
@login_required
def list(table):
    if table == "registrations":
        ev_list = event_list()
        evlist = vars(ev_list)
        evlist = [val for evlist in evlist.values() for val in evlist]
        list = [(str(ev_id), ev_name) for ev_id, ev_name, ev_amt, ev_solo, ev_duo, ev_squad, ev_team, ev_team_participants in evlist]
        set_evlist(list)
        session['evlist'] = evlist
        rows = registrations.query.all()
        return render_template("list_registrations.html", rows=rows, evlist=evlist)
    elif table == "payments":
        rows = payments.query.all()
        return render_template("list_payments.html", rows=rows)
    