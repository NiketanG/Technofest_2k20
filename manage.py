from flask.cli import FlaskGroup
from app.models import events, users, registrations
from app import create_app,db

import redis
from rq import Connection, Worker
import os
import time
from dotenv import load_dotenv
load_dotenv()
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

if __name__ == '__main__':
    cli()