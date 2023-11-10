import os

from flask import Flask

def create_app():
    mailer = Flask(__name__)

    mailer.config.from_mapping(
        FROM_EMAIL=os.environ.get('FROM_EMAIL'),
        GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )

    from . import db

    db.init_app(mailer)

    from . import mail

    mailer.register_blueprint(mail.bp)

    return mailer
