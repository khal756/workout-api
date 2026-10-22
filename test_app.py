
import pytest
from datetime import date
from app import app
from extensions import db
from models import Exercise, Workout, WorkoutExercise


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        exercise = Exercise(
            name="Push-up",
            category="Strength",
            equipment_needed=False
        )
        workout = Workout(
            date=date(2026, 10, 23),
            duration_minutes=30,
            notes="Test workout"
        )
        db.session.add_all([exercise, workout])
        db.session.commit()

        db.session.add(
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercise.id,
                reps=10,
                sets=3,
                duration_seconds=30
            )
        )
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_get_workouts(client):
    response = client.get("/workouts")
    assert response.status_code == 200


def test_get_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200


def test_get_workout_by_id(client):
    response = client.get("/workouts/1")
    assert response.status_code == 200


def test_get_exercise_by_id(client):
    response = client.get("/exercises/1")
    assert response.status_code == 200


def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-10-24",
            "duration_minutes": 45,
            "notes": "Evening workout"
        }
    )
    assert response.status_code in (200, 201)


def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Squat",
            "category": "Strength",
            "equipment_needed": False
        }
    )
    assert response.status_code in (200, 201)


def test_reject_invalid_workout_duration():
    with pytest.raises(ValueError):
        Workout(date=date(2026, 10, 23), duration_minutes=0)


def test_reject_blank_exercise_name():
    with pytest.raises(ValueError):
        Exercise(
            name="   ",
            category="Strength",
            equipment_needed=False
        )


def test_reject_invalid_reps():
    with pytest.raises(ValueError):
        WorkoutExercise(
            workout_id=1,
            exercise_id=1,
            reps=0,
            sets=3
        )
