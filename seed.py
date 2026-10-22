
from datetime import date

from app import app
from extensions import db
from models import Exercise, Workout, WorkoutExercise


def seed_database():
    with app.app_context():
        exercise = Exercise.query.filter_by(name="Push-up").first()

        if exercise is None:
            exercise = Exercise(
                name="Push-up",
                category="Strength",
                equipment_needed=False
            )
            db.session.add(exercise)
            db.session.flush()

        workout = Workout.query.filter_by(
            date=date.today(),
            notes="Sample seeded workout"
        ).first()

        if workout is None:
            workout = Workout(
                date=date.today(),
                duration_minutes=30,
                notes="Sample seeded workout"
            )
            db.session.add(workout)
            db.session.flush()

        association = WorkoutExercise.query.filter_by(
            workout_id=workout.id,
            exercise_id=exercise.id
        ).first()

        if association is None:
            association = WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercise.id,
                reps=10,
                sets=3,
                duration_seconds=30
            )
            db.session.add(association)

        db.session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
