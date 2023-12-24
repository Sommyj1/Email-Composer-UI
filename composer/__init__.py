from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import timedelta
from flask_mailman import Mail

db = SQLAlchemy()

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Email-Composer'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MY_DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Initilizaing Flask-mailman
    mail.init_app(app)

    # session timeout
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # Keep Sessions Alive
    @app.before_request
    def session_timeout():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=1)
    
    # Registering all blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all(app=app)
        print('Created Database!')