from marshmallow import Schema, fields

from code_.app.core.database import ma
from code_.app.models import Word


class BaseWordSchema(ma.SQLAlchemyAutoSchema):
    title_uz = fields.String(required=True)
    title_ru = fields.String(required=True)
    title_en = fields.String(required=True)

    class Meta:
        model = Word


class ReadWordSchema(ma.SQLAlchemyAutoSchema):
    # id = fields.Integer(required=True)
    # created_at = fields.DateTime(dump_only=True, required=True)
    # updated_at = fields.DateTime(dump_only=True)

    class Meta:
        model = Word
        # fields = ('forename', 'surname', 'birthday', ...)


class CreateWordSchema(BaseWordSchema):
    pass


class UpdateWordSchema(BaseWordSchema):
    pass
