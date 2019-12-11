from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField,
                     SelectField,
                     RadioField,
                     PasswordField,
                     BooleanField,
                     IntegerField)
from wtforms.validators import (DataRequired,
                                InputRequired,
                                Email,
                                EqualTo,
                                Length,
                                Regexp,
                                ValidationError)
from app import db
from app.models import events

list = list()
def set_evlist(eventlist):
    list.clear()
    list.insert(0, ('0', 'Select Event :'))
    list.extend(eventlist)

class RegistrationForm(FlaskForm):   
    name = StringField('Name : ', [DataRequired("Name cannot be left blank")], render_kw={"placeholder": "Severus Snape", "id": "name"})

    phno = StringField('Phone No. :', [DataRequired("Phone no. cannot be left blank")], render_kw={
                       "placeholder": "605 475 6961", "id": "PhNo", "maxlength": "10"})

    email = StringField('Email Address : ', [
        Email('Not a valid email address.'),
        DataRequired("Email Address cannot be left blank")], render_kw={"placeholder": "Severus Snape", "id": "email"})

    clgname = StringField('Institute Name : ', [DataRequired("College Name cannot be left blank")], render_kw={
                          "placeholder": "Hogwarts School of Witchcraft and Wizardry", "id": "ClgName"})

    event = SelectField('Event to participate in : ', [DataRequired()],
                        choices=list, render_kw={"id": "events"})

    radio_team = RadioField('No. of Participants : ', [DataRequired()],
                            choices=[('1', 'Solo ( 1 )'),
                                     ('2', 'Duo ( 2 )'),
                                     ('4', 'Squad ( 4 )')], default='1', render_kw={"id": "radio_team"})

    GrpName = StringField('Group Name : ', render_kw={
                          "placeholder": "Gryffindor", "class": "inputs grp", "id": "GrpName"})

    submit = SubmitField('REGISTER')

    submit_ofc = SubmitField('REGISTER ( Pay via Cash )')

