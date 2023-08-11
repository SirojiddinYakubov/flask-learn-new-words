import datetime

from code_.app.core.database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now(), default=db.func.now())

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
