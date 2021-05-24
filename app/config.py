import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    MID = os.getenv('MID')
    MERCHANT_KEY = os.getenv('MERCHANT_KEY')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    WEBSITE = os.getenv('WEBSITE')
    PAYMENT_URL = os.getenv('PAYMENT_URL')
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS'))
    REDIS_URL = os.getenv('REDIS_URL')
    QUEUES = os.getenv('QUEUES')
    
    AUTH_CODE = os.getenv('AUTH_CODE')
    SESSION_COOKIE_HTTPONLY=True
