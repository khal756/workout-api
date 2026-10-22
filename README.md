
# Flask SQLAlchemy Workout Application Backend

## Description

A REST API built with Flask, SQLAlchemy, Marshmallow, and Flask-Migrate. It manages workouts, exercises, and the exercises performed during each workout.

## Features

- Create, list, retrieve, and delete workouts.
- Create, list, retrieve, and delete exercises.
- Associate exercises with workouts.
- Validate incoming data using Marshmallow schemas.
- Enforce data integrity using model validations and database constraints.
- Manage database schema changes with Flask-Migrate.
- Populate the database with sample data using a seed script.

## Technologies

- Python 3.12
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Marshmallow
- Flask-Migrate
- SQLite
- Pytest

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/khal756/workout-api.git
   cd workout-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install Pipenv and project dependencies:

   ```bash
   python -m pip install pipenv
   python -m pipenv install
   ```

4. Apply database migrations:

   ```bash
   python -m pipenv run flask --app app db upgrade
   ```

5. Seed the database:

   ```bash
   python -m pipenv run python seed.py
   ```

## Running the application

Start the Flask development server:

```bash
python -m pipenv run flask --app app run --debug
```

The API will normally be available at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List workouts |
| GET | `/workouts/<id>` | Retrieve a workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List exercises |
| GET | `/exercises/<id>` | Retrieve an exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

### Example: Create a workout

Send a POST request to `/workouts` with JSON:

```json
{
  "date": "2026-10-23",
  "duration_minutes": 30,
  "notes": "Morning workout"
}
```

### Example: Create an exercise

Send a POST request to `/exercises` with JSON:

```json
{
  "name": "Push-up",
  "category": "Strength",
  "equipment_needed": false
}
```

## Testing

Install pytest if necessary:

```bash
python -m pipenv run python -m pip install pytest
```

Run the test suite:

```bash
python -m pipenv run python -m pytest -q
```

## Database and validation

Database migrations are stored in the `migrations/` directory. The application uses Marshmallow schema validation, SQLAlchemy model validation, and database check constraints to protect data integrity.

## License

This project was created as a learning and assessment project.
