from flask import Flask, jsonify, request
from extensions import db
from flask_migrate import Migrate
from marshmallow import Schema, fields, validate, validates, ValidationError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

from models import Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema

@app.route("/exercises", methods=["GET"])
def exercise_records():
    exercises=Exercise.query.all()
    exercise_list=ExerciseSchema(many=True).dump(exercises)
    return jsonify(exercise_list)

if __name__ == "__main__":
    app.run(debug=True)