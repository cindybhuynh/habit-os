"""create habits

Revision ID: 60d175827b43
Revises:
Create Date: 2026-01-07 12:48:12.664833
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "60d175827b43"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "habits",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("schedule_type", sa.String(), nullable=False),
        sa.Column("target_count", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("notes", sa.String(), nullable=True),

        sa.UniqueConstraint("name", name="uq_habits_name"),
        sa.CheckConstraint("target_count >= 1", name="ck_habits_target_count_ge1"),
        sa.CheckConstraint(
            "schedule_type IN ('daily', 'weekly')",
            name="ck_habits_schedule_type_valid",
        ),
    )


def downgrade() -> None:
    op.drop_table("habits")
