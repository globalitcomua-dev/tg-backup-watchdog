"""add backup_states table

Revision ID: 0002_backup_states
Revises: 0001_create_core_tables
Create Date: 2026-06-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_backup_states"
down_revision: Union[str, None] = "0001_create_core_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "backup_states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("host", sa.String(length=255), nullable=False),
        sa.Column("job", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column(
            "last_changed_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "last_notified_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_backup_states_host",
        "backup_states",
        ["host"],
    )

    op.create_index(
        "ix_backup_states_job",
        "backup_states",
        ["job"],
    )

    op.create_unique_constraint(
        "uq_backup_state",
        "backup_states",
        ["host", "job"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_backup_state",
        "backup_states",
        type_="unique",
    )

    op.drop_index(
        "ix_backup_states_job",
        table_name="backup_states",
    )

    op.drop_index(
        "ix_backup_states_host",
        table_name="backup_states",
    )

    op.drop_table("backup_states")