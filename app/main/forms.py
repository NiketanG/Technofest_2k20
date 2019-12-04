
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField,
                     SelectField,
                     RadioField,
                     PasswordField,
                     BooleanField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL,
                                ValidationError)
from app import db
from app.models import events

list = list()
def set_evlist(eventlist):
    list.clear()
    list.insert(0, ('0', 'Select Event :'))
    list.extend(eventlist)

class RegistrationForm(FlaskForm):   
    name = StringField('Name : ', [
        DataRequired()], render_kw={"placeholder": "Severus Snape", "class": "inputs", "id": "name"})

    phno = StringField('Phone No. :', [DataRequired(message="Phone no. cannot be left blank")], render_kw={
                       "placeholder": "(605) 475-6961", "class": "inputs", "id": "PhNo", "required": '', "maxlength": "10"})

    email = StringField('Email Address : ', [
        Email(message='Not a valid email address.'),
        DataRequired()], render_kw={"placeholder": "Severus Snape", "class": "inputs", "id": "email"})

    clgname = StringField('Institute Name : ', [DataRequired()], render_kw={
                          "placeholder": "Hogwarts School of Witchcraft and Wizardry", "class": "inputs", "id": "ClgName"})

    event = SelectField('Event to participate in : ', [DataRequired()],
                        choices=list, render_kw={"id": "events", "class": "inputs"})

    radio_team = RadioField('No. of Participants : ', [DataRequired()],
                            choices=[('1', 'Solo ( 1 )'),
                                     ('2', 'Duo ( 2 )'),
                                     ('4', 'Squad ( 4 )')], default='1', render_kw={"id": "radio_team"})

    GrpName = StringField('Group Name : ', render_kw={
                          "placeholder": "Gryffindor", "class": "inputs grp", "id": "GrpName"})

    submit = SubmitField('REGISTER', render_kw={
                         "class": "registerbtn", "id": "registerbtn", "disabled": ''})

    submit_ofc = SubmitField('REGISTER ( Pay via Cash )', render_kw={
        "class": "registerbtn", "id": "registerbtn2", "disabled": ''})

