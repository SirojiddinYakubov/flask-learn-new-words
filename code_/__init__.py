from flask import Flask
from code_.app.models import *  # noqa
from code_.app.core.config import Config, BASE_DIR
from code_.app.core.database import db, migrate, ma
from code_.app.word.routers import word_blueprint

app = Flask(__name__, template_folder=f'{BASE_DIR}/code_/app/templates', static_folder=f'{BASE_DIR}/code_/app/static')
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

# app.register_blueprint(word_blueprint, url_prefix="/word")
app.register_blueprint(word_blueprint)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
