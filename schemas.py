from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    name = fields.String(validate.Length(min=1), required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean(required=True)