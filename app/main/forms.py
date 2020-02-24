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
ev_participants = []

def set_evlist(eventlist):
    list.clear()
    list.insert(0, ('0', 'Select Event :'))
    list.extend(eventlist)
    ev_participants.clear()
    prt = events.query.filter(events.team_participants!=None).all()
    ev_participants.extend([('1', 'Solo ( 1 )'), ('2', 'Duo ( 2 )'), ('4', 'Squad ( 4 )')])
    for row in prt:
        row = row.__dict__
        ev_participants.append((str(row["team_participants"]), "Team ("+ str(row["team_participants"]) +")"))

class RegistrationForm(FlaskForm):   
    name = StringField('Name : ', [DataRequired("Name cannot be left blank")], render_kw={"placeholder": "Severus Snape", "id": "name", "maxlength": "25"})

    phno = StringField('Phone No. :', [DataRequired("Phone no. cannot be left blank")], render_kw={
                       "placeholder": "605 475 6961", "id": "PhNo", "maxlength": "10"})

    email = StringField('Email Address : ', [
        Email('Not a valid email address.'),
        DataRequired("Email Address cannot be left blank")], render_kw={"placeholder": "Severus@hogwarts.edu", "id": "email","maxlength": "30"})

    clgname = StringField('Institute Name : ', [DataRequired("College Name cannot be left blank")], render_kw={"placeholder": "Hogwarts School of Witchcraft and Wizardry", "id": "ClgName", "maxlength": "25"})

    event = SelectField('Event to participate in : ', [DataRequired()], choices=list, render_kw={"id": "events"})

    radio_team = RadioField('No. of Participants : ', [DataRequired()],
                            choices=ev_participants, default='1', render_kw={"id": "radio_team"})

    GrpName = StringField('Group Name : ', render_kw={
                          "placeholder": "Gryffindor", "class": "inputs grp", "id": "GrpName",  "maxlength": "20"})

    submit = SubmitField('REGISTER')

    submit_ofc = SubmitField('REGISTER ( Pay via Cash )')

