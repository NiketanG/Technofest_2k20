import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    MID = os.getenv('MID')
    MERCHANT_KEY = os.getenv('MERCHANT_KEY')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    WEBSITE = os.getenv('WEBSITE')
    PAYMENT_URL = os.getenv('PAYMENT_URL')
    BCRYPT_LOG_ROUNDS = 5
    REDIS_URL = os.getenv('REDIS_URL')
    QUEUES = ['default']
    
    #SESSION_COOKIE_SECURE=False
    SESSION_COOKIE_HTTPONLY=True
    #PERMANENT_SESSION_LIFETIME=6