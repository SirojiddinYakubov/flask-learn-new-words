from flask import Flask
from code_.app.models import *  # noqa
from code_.app.core.config import Config
from code_.app.core.database import db, migrate


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)
