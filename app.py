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

@app.route("/exercises/<int:id>", methods=["GET"])
def find_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    exercise_details = ExerciseSchema().dump(exercise)
    return jsonify(exercise_details)

@app.route("/exercises", methods= ["POST"])
def create_exercise():
    data = request.get_json()
    try:
        validated_data = ExerciseSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messeges}), 400
    
    exercise = Exercise(**validated_data)
    db.session.add(exercise)
    db.session.commit()

    exercise_details = ExerciseSchema().dump(exercise)
    return jsonify(exercise_details), 201

@app.route("/exercises", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)