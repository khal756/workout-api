
from extensions import db
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_exercise_name_not_empty"
        ),
        CheckConstraint(
            "length(trim(category)) > 0",
            name="check_exercise_category_not_empty"
        ),
    )

    @validates("name", "category")
    def validate_nonblank_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} cannot be empty or blank")
        return value.strip()

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration_positive"
        ),
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
        ):
            raise ValueError(
                "Workout duration must be a positive integer"
            )
        return value

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )


class WorkoutExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workout.id"),
        nullable=False
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercise.id"),
        nullable=False
    )

    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "reps > 0",
            name="check_workout_exercise_reps_positive"
        ),
        CheckConstraint(
            "sets > 0",
            name="check_workout_exercise_sets_positive"
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="check_workout_exercise_duration_nonnegative"
        ),
    )

    @validates("reps", "sets")
    def validate_positive_count(self, key, value):
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
        ):
            raise ValueError(f"{key} must be a positive integer")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < 0
        ):
            raise ValueError(
                "Duration seconds must be a non-negative integer or None"
            )
        return value

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )
    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )
