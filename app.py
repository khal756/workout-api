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
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

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
        return jsonify({"errors": err.messages}), 400
    
    exercise = Exercise(**validated_data)
    db.session.add(exercise)
    db.session.commit()

    exercise_details = ExerciseSchema().dump(exercise)
    return jsonify(exercise_details), 201

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return "", 204

@app.route("/workouts", methods=["GET"])
def workouts_record():
    workouts = Workout.query.all()
    workout_list = WorkoutSchema(many=True).dump(workouts)
    return jsonify(workout_list)

@app.route("/workouts/<int:id>", methods=["GET"])
def find_workout(id):
    workout = Workout.query.get_or_404(id)
    workout_details = WorkoutSchema().dump(workout)
    return jsonify(workout_details)

@app.route("/workouts", methods= ["POST"])
def create_workout():
    data = request.get_json()
    try:
        validated_data= WorkoutSchema().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    workout = Workout(**validated_data)
    db.session.add(workout)
    db.session.commit()

    workout_details= WorkoutSchema().dump(workout)
    return jsonify(workout_details), 201

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout =Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return "", 204

@app.route("/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises", methods=["POST"])
def create_workout_exercise(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    data = request.get_json()
    try:
        validated_data = WorkoutExerciseSchema().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    workoutexercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id= exercise.id,
        reps=validated_data["reps"],
        sets=validated_data["sets"],
        duration_seconds=validated_data.get("duration_seconds")
        )
    db.session.add(workoutexercise)
    db.session.commit()

    workoutexercise_details = WorkoutExerciseSchema().dump(workoutexercise)
    return jsonify(workoutexercise_details), 201



if __name__ == "__main__":
    app.run(debug=True)