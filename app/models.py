from flask import Flask, current_app, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz  # For localizing time
from app import db, login_manager
from flask_login import UserMixin

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('user.login'))

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class events(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(20), nullable=True)
    amt_per_head = db.Column(db.Integer, nullable=False)
    solo = db.Column(db.Boolean, nullable=False, default=True)
    duo = db.Column(db.Boolean, nullable=False, default=True)
    squad = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"events({self.event_id}, '{self.event_name}', {self.amt_per_head}, {self.solo}, {self.duo}, {self.squad})"
    
    def __init__(self, event_name, amt_per_head, solo, duo, squad):
        self.event_name = event_name
        self.amt_per_head = amt_per_head
        self.solo = solo
        self.duo = duo
        self.squad = squad

    def serialize(self):
        return {
            self.event_id,
            self.event_name,
            self.amt_per_head,
            self.solo,
            self.duo,
            self.squad,
        }

class registrations(db.Model):
    __tablename__ = 'registrations'
    reg_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    clgname = db.Column(db.String(30), nullable=False)
    phno = db.Column(db.BigInteger, nullable=False)
    grpname = db.Column(db.String(20), nullable=True)
    event_id = db.Column(db.Integer, nullable=False)
    team = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(20), nullable=False)
    # r_user = db.relationship('users', backref='username', lazy=True)
    date_registered = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    paid = db.Column(db.Boolean, default=False, nullable=False)
    order_id = db.Column(db.String, nullable=False, unique=True)
    cust_id = db.Column(db.String, nullable=False)
    amt = db.Column(db.Integer, nullable=False)
    paymentmode=db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"Registration('{self.name}', '{self.email}' , '{self.clgname}', '{self.phno}', '{self.grpname}', '{self.event_id}', '{self.team}', '{self.user}', '{self.date_registered}', '{self.paid}', '{self.order_id}', '{self.cust_id}', '{self.amt}', '{self.paymentmode}')"

    def __init__(self, **entries):
        self.__dict__.update(entries)

class users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}' , '{self.email}')"

    def get_id(self):
        return (self.user_id)

class payments(db.Model):
    __tablename__='payments'
    txn_id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String, nullable=False)
    txn_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    resp_code = db.Column(db.Integer, nullable=False)
    resp_msg = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"payments('{self.txn_id}', '{self.order_id}', '{self.txn_amount}', '{self.status}', '{self.resp_code}', '{self.resp_msg}')"

    def __init__(self, **entries):
        self.__dict__.update(entries)