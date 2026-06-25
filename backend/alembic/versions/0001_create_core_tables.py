"""create core tables

Revision ID: 0001_create_core_tables
Revises:
Create Date: 2026-06-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_create_core_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "backup_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("host", sa.String(length=255), nullable=False),
        sa.Column("job", sa.String(length=255), nullable=False),
        sa.Column("engine", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("backup_type", sa.String(length=100), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=True),
        sa.Column("error_count", sa.Integer(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("snapshot_id", sa.String(length=255), nullable=True),
        sa.Column("destination", sa.String(length=500), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("raw_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_backup_runs_host", "backup_runs", ["host"])
    op.create_index("ix_backup_runs_job", "backup_runs", ["job"])
    op.create_index("ix_backup_runs_engine", "backup_runs", ["engine"])
    op.create_index("ix_backup_runs_status", "backup_runs", ["status"])
    op.create_index("ix_backup_runs_created_at", "backup_runs", ["created_at"])

    op.create_table(
        "backup_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("host", sa.String(length=255), nullable=False),
        sa.Column("job", sa.String(length=255), nullable=False),
        sa.Column("engine", sa.String(length=100), nullable=False),
        sa.Column("expected_every_hours", sa.Integer(), nullable=False, server_default="24"),
        sa.Column("deadline", sa.String(length=20), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_backup_jobs_host", "backup_jobs", ["host"])
    op.create_index("ix_backup_jobs_job", "backup_jobs", ["job"])
    op.create_index("ix_backup_jobs_engine", "backup_jobs", ["engine"])
    op.create_index("ix_backup_jobs_created_at", "backup_jobs", ["created_at"])
    op.create_unique_constraint("uq_backup_jobs_host_job", "backup_jobs", ["host", "job"])

    op.create_table(
        "telegram_offsets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("bot_name", sa.String(length=100), nullable=False),
        sa.Column("last_update_id", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_telegram_offsets_bot_name", "telegram_offsets", ["bot_name"], unique=True)
    op.create_index("ix_telegram_offsets_updated_at", "telegram_offsets", ["updated_at"])


def downgrade() -> None:
    op.drop_index("ix_telegram_offsets_updated_at", table_name="telegram_offsets")
    op.drop_index("ix_telegram_offsets_bot_name", table_name="telegram_offsets")
    op.drop_table("telegram_offsets")

    op.drop_constraint("uq_backup_jobs_host_job", "backup_jobs", type_="unique")
    op.drop_index("ix_backup_jobs_created_at", table_name="backup_jobs")
    op.drop_index("ix_backup_jobs_engine", table_name="backup_jobs")
    op.drop_index("ix_backup_jobs_job", table_name="backup_jobs")
    op.drop_index("ix_backup_jobs_host", table_name="backup_jobs")
    op.drop_table("backup_jobs")

    op.drop_index("ix_backup_runs_created_at", table_name="backup_runs")
    op.drop_index("ix_backup_runs_status", table_name="backup_runs")
    op.drop_index("ix_backup_runs_engine", table_name="backup_runs")
    op.drop_index("ix_backup_runs_job", table_name="backup_runs")
    op.drop_index("ix_backup_runs_host", table_name="backup_runs")
    op.drop_table("backup_runs")