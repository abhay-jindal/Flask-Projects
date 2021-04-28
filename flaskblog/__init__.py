from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from celery import Celery


def make_celery(app=None):
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend="redis://localhost:6379/0",
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, include=["app.module1.service"])


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    celery = make_celery(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    from flaskblog.books.routes import books
    from flaskblog.reminder.routes import reminder

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(books)
    app.register_blueprint(reminder)

    return app
