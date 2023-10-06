from .base_model import BaseModel
from app.core.database import db, session
from flask_login import UserMixin


class User(UserMixin, BaseModel):
    __tablename__ = 'user'

    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
