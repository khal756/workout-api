from extensions import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False )
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)
    workout_exercises = db.relationship("WorkoutExercise")
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    workout_exercises = db.relationship("WorkoutExercise")

class WorkoutExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id =db.Column(db.Integer, db.ForeignKey("workout.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds= db.Column(db.Integer, nullable=True)
    workout = db.relationship("Workout")
    exercise = db.relationship("Exercise")