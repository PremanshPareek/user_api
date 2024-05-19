import logging

from flask import Flask

from user_api.routes import users
from user_api.database.db import db
from user_api.config import Config

def create_app(app_config=None):
    app = Flask(__name__)

    if app_config is None:
        app.config.from_object(Config)



    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


    app.register_blueprint(users.bp)
    return app