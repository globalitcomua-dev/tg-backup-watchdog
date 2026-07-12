"""add producer_credentials table

Revision ID: 0003_producer_credentials
Revises: 0002_backup_states
Create Date: 2026-07-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_producer_credentials"
down_revision: Union[str, None] = "0002_backup_states"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "producer_credentials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("producer_name", sa.String(length=100), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("allowed_hosts", sa.JSON(), nullable=False),
        sa.Column("allowed_jobs", sa.JSON(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_producer_credentials_id",
        "producer_credentials",
        ["id"],
    )
    op.create_index(
        "ix_producer_credentials_producer_name",
        "producer_credentials",
        ["producer_name"],
        unique=True,
    )
    op.create_index(
        "ix_producer_credentials_token_hash",
        "producer_credentials",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_producer_credentials_created_at",
        "producer_credentials",
        ["created_at"],
    )
    op.create_index(
        "ix_producer_credentials_updated_at",
        "producer_credentials",
        ["updated_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_producer_credentials_updated_at", table_name="producer_credentials")
    op.drop_index("ix_producer_credentials_created_at", table_name="producer_credentials")
    op.drop_index("ix_producer_credentials_token_hash", table_name="producer_credentials")
    op.drop_index("ix_producer_credentials_producer_name", table_name="producer_credentials")
    op.drop_index("ix_producer_credentials_id", table_name="producer_credentials")
    op.drop_table("producer_credentials")
