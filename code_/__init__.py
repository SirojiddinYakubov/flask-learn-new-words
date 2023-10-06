from flask import Flask
from app.models import *  # noqa
from app.core.config import Config, BASE_DIR
from app.core.database import db, migrate, ma, session
from app.word.routers import word_blueprint
from flask_moment import Moment

app = Flask(__name__, template_folder=f'{BASE_DIR}/code_/app/templates', static_folder=f'{BASE_DIR}/code_/app/static')
moment = Moment()
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False
db.init_app(app)
ma.init_app(app)
moment.init_app(app)
migrate.init_app(app, db)

# app.register_blueprint(word_blueprint, url_prefix="/word")
app.register_blueprint(word_blueprint)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
