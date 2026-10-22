from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    name = fields.String(validate=validate.Length(min=1), required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean(required=True)

class WorkoutSchema(Schema):
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(validate=validate.Range(min=1),required=True)
    notes = fields.String(allow_none=True, required=False)

class WorkoutExerciseSchema(Schema):
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(validate=validate.Range(min=1), required=True)
    sets = fields.Integer(validate=validate.Range(min=1),required=True)
    duration_seconds = fields.Integer(validate=validate.Range(min=0), required=False, allow_none=True)