from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import Schema, fields, validate, validates, ValidationError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Exercise, Workout, WorkoutExercise