"""add validation check constraints

Revision ID: 4ff6441dc820
Revises: d3fa36abd329
Create Date: 2026-10-23 01:41:03.546392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ff6441dc820'
down_revision = 'd3fa36abd329'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("exercise") as batch_op:
        batch_op.create_check_constraint(
            "check_exercise_name_not_empty",
            "length(trim(name)) > 0"
        )
        batch_op.create_check_constraint(
            "check_exercise_category_not_empty",
            "length(trim(category)) > 0"
        )

    with op.batch_alter_table("workout") as batch_op:
        batch_op.create_check_constraint(
            "check_workout_duration_positive",
            "duration_minutes > 0"
        )

    with op.batch_alter_table("workout_exercise") as batch_op:
        batch_op.create_check_constraint(
            "check_workout_exercise_reps_positive",
            "reps > 0"
        )
        batch_op.create_check_constraint(
            "check_workout_exercise_sets_positive",
            "sets > 0"
        )
        batch_op.create_check_constraint(
            "check_workout_exercise_duration_nonnegative",
            "duration_seconds IS NULL OR duration_seconds >= 0"
        )


def downgrade():
    with op.batch_alter_table("workout_exercise") as batch_op:
        batch_op.drop_constraint(
            "check_workout_exercise_duration_nonnegative",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_workout_exercise_sets_positive",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_workout_exercise_reps_positive",
            type_="check"
        )

    with op.batch_alter_table("workout") as batch_op:
        batch_op.drop_constraint(
            "check_workout_duration_positive",
            type_="check"
        )

    with op.batch_alter_table("exercise") as batch_op:
        batch_op.drop_constraint(
            "check_exercise_category_not_empty",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_exercise_name_not_empty",
            type_="check"
        )
