from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_compress import Compress
from flask_caching import Cache
from flask_assets import Environment, Bundle

import rq
from redis import Redis
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
#login_manager.session_protection = "strong"
mail = Mail()
compress = Compress()
cache = Cache(config={'CACHE_TYPE': 'simple'})
assets = Environment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue(app.config['QUEUES'], connection=app.redis)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    compress.init_app(app)
    cache.init_app(app)
    assets.init_app(app)
    
    from app.user.routes import user
    from app.main.routes import main
    from app.other.routes import other
    from app.errors.handlers import errors
    app.register_blueprint(user)
    app.register_blueprint(main)
    app.register_blueprint(other)
    app.register_blueprint(errors)

    return app