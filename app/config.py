import os

class Config:
    SECRET_KEY = '57bde4dd-0da1-41dd-b5bc-38d5997d0fc1'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    #'postgresql://postgres:N!kketanGT16@localhost/comeit_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'comeit2k19@gmail.com'
    MAIL_PASSWORD = 'COMeIT2k19'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = 'comeit2k19@gmail.com'

    MID = 'LmKkyo30678627278847'
    MERCHANT_KEY = 'qPi6D9SNG6faAdLn'
    CHANNEL_ID = 'WEB'
    WEBSITE = 'DEFAULT'
    PAYMENT_URL = 'https://securegw.paytm.in/order/'
    BCRYPT_LOG_ROUNDS = 5
    REDIS_URL = 'redis://localhost:6379/0'
    QUEUES = ['default']
    
    AUTH_CODE = 'COMeIT_TF_2020'
    #SESSION_COOKIE_SECURE=False
    SESSION_COOKIE_HTTPONLY=True
    #PERMANENT_SESSION_LIFETIME=6