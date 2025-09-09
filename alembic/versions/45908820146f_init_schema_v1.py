"""init schema v1

Revision ID: 45908820146f
Revises: 
Create Date: 2025-09-09 13:03:36.636255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import CHAR


# revision identifiers, used by Alembic.
revision: str = '45908820146f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # participants
    op.create_table(
        "participants",
        sa.Column("id", CHAR(32), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consent_version", sa.String(32), nullable=True),
        sa.Column("consent_accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locale", sa.String(16), nullable=True),
        sa.Column("user_agent_hash", sa.String(64), nullable=True),
        sa.Column("cohort", sa.String(32), nullable=True),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    # sessions
    op.create_table(
        "sessions",
        sa.Column("id", CHAR(32), primary_key=True),
        sa.Column("participant_id", CHAR(32), sa.ForeignKey("participants.id"), nullable=False),
        sa.Column("mode", sa.String(8), nullable=False),
        sa.Column("agent_skill", sa.String(16), nullable=True),
        sa.Column("game_version", sa.String(64), nullable=True),
        sa.Column("model_version", sa.String(64), nullable=True),
        sa.Column("seed", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("result", sa.JSON(), nullable=True),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_sessions_participant", "sessions", ["participant_id"]) 

    # events
    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger().with_variant(sa.BigInteger(), "mysql"), primary_key=True, autoincrement=True),
        sa.Column("session_id", CHAR(32), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("t_ms", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_events_session_t", "events", ["session_id", "t_ms"]) 

    # replays
    op.create_table(
        "replays",
        sa.Column("id", CHAR(32), primary_key=True),
        sa.Column("session_id", CHAR(32), sa.ForeignKey("sessions.id"), nullable=False, unique=True),
        sa.Column("storage_url", sa.Text(), nullable=False),
        sa.Column("frames_count", sa.Integer(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("compression", sa.String(16), nullable=True),
        sa.Column("schema_version", sa.String(16), nullable=True),
        sa.Column("generated_by", sa.String(16), nullable=True),
        sa.Column("checksum", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    # experiments
    op.create_table(
        "experiments",
        sa.Column("id", CHAR(32), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    # assignments
    op.create_table(
        "assignments",
        sa.Column("id", CHAR(32), primary_key=True),
        sa.Column("experiment_id", CHAR(32), sa.ForeignKey("experiments.id"), nullable=False),
        sa.Column("participant_id", CHAR(32), sa.ForeignKey("participants.id"), nullable=False),
        sa.Column("arm", sa.String(32), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    # consents
    op.create_table(
        "consents",
        sa.Column("version", sa.String(32), primary_key=True),
        sa.Column("document_url", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )


def downgrade() -> None:
    op.drop_table("consents")
    op.drop_table("assignments")
    op.drop_table("experiments")
    op.drop_table("replays")
    op.drop_index("ix_events_session_t", table_name="events")
    op.drop_table("events")
    op.drop_index("ix_sessions_participant", table_name="sessions")
    op.drop_table("sessions")
    op.drop_table("participants")
