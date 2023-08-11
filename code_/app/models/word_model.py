import datetime

from code_.app.core.database import db, session
from .base_model import BaseModel


class Word(BaseModel):
    __tablename__ = 'word'

    id = db.Column(db.Integer, primary_key=True)
    title_uz = db.Column(db.String)
    title_ru = db.Column(db.String)
    title_en = db.Column(db.String)

    @classmethod
    def get_list(cls, start: datetime.date, stop: datetime.date) -> list["Word"]:
        words = cls.query.all()
        session.commit()
        return words

    @classmethod
    def get(cls, obj_id: int) -> "Word":
        stmt = cls.query.filter(Word.id == obj_id)
        word = session.execute(stmt).scalar_one_or_none()
        return word

    @classmethod
    def create(cls, data: dict) -> "Word":
        obj = Word(**data)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def update(cls, obj_id: int, data: dict) -> "Word":
        obj = cls.get(obj_id)
        for key, value in data.items():
            setattr(obj, key, value)
        session.merge(obj)
        session.commit()
        return obj

    @classmethod
    def delete(cls, obj_id: int) -> None:
        obj = cls.get(obj_id)
        session.delete(obj)
        session.commit()

    def __repr__(self):
        return f'<Word {self.id}>'
