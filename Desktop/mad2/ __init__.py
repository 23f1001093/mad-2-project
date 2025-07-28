from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery
from .celery import make_celery

db = SQLAlchemy()
mail = Mail()
celery = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    mail.init_app(app)

    global celery
    celery = make_celery(app)

    # Import routes so they register with the app
    from . import routes
    app.register_blueprint(routes.bp)

    return app
