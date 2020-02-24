from dotenv import load_dotenv
load_dotenv()
from flask.cli import FlaskGroup
from app.models import events, users, registrations
from app import create_app,db, bcrypt
import redis
from rq import Connection, Worker
import os
import time
import uuid

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('run_worker')
def run_worker():
    try:
        redis_url = app.config['REDIS_URL']
        redis_connection = redis.from_url(redis_url)
        with Connection(redis_connection):
            worker = Worker(app.config['QUEUES'])
            worker.work()
    except redis.exceptions.ConnectionError or redis.exceptions.ConnectionRefusedError:
        print("run this command first : python manage.py run_redis ")
    
@cli.command('run_redis')
def run_redis():
    print("Launching redis-server. Please wait.")
    print("Execute the following command in a new terminal window : \n\npython manage.py run_worker")
    time.sleep(5)
    os.system("redis-server")

@cli.command('create_db')
def create_db():
    db.create_all()
    db.session.commit()
    print('Database Created')

@cli.command('create_user')
def create_user():
    username = str(input("Enter usename : "))
    name = str(input("Enter Name : "))
    email = str(input("Enter email address : "))
    password = str(input("Enter a password : "))
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = users(username=username,
                        name=name,
                        email=email,
                        password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print('User created. Now you can login.')

@cli.command('create_events')
def create_events():
    for i in range(1,100):
        print("Event " + str(i))
        event_name = str(input("Enter Event Name : "))
        amt = str(input("Enter Amount: "))
        solo = int(input("SOLO Participation : (1 or 0) : "))
        duo = int(input("DUO Participation : (1 or 0) : "))
        squad = int(input("SQUAD Participation : (1 or 0) : "))
        team = int(input("Team Participation : (1 or 0) : "))
        if (team == 1):
            team_participants = int(input("Team Participants Count : "))
        else:
            team_participants = None

        event = events(event_name=event_name,amt=amt,solo=solo,duo=duo,squad=squad, team=team, team_participants=team_participants)
        db.session.add(event)
        db.session.commit()

        print('Event Added')

        ch = str(input("Press X to exit. Else Press Enter"))
        if (ch == 'X' or ch == 'x'):
            break

if __name__ == '__main__':
    cli()