from flask import Flask
from app.models import *  # noqa
from app.core.config import Config, BASE_DIR, config
from app.core.database import db, migrate, ma, session
from app.word.routers import word_blueprint
from flask_moment import Moment
from flask_session import Session
from flask_login import LoginManager

from auth.routers import auth_blueprint

app = Flask(__name__, template_folder=f'{BASE_DIR}/code_/app/templates', static_folder=f'{BASE_DIR}/code_/app/static')
moment = Moment()
sess = Session()
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = config.SECRET_KEY
sess.init_app(app)
db.init_app(app)
ma.init_app(app)
moment.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# app.register_blueprint(word_blueprint, url_prefix="/word")
app.register_blueprint(word_blueprint)
app.register_blueprint(auth_blueprint)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
