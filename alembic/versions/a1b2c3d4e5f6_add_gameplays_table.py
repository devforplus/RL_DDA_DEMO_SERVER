"""add gameplays table

Revision ID: a1b2c3d4e5f6
Revises: 96a09501951b
Create Date: 2025-10-14 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "96a09501951b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create gameplays table
    op.create_table(
        "gameplays",
        sa.Column("id", mysql.CHAR(32), nullable=False),
        sa.Column("nickname", sa.String(length=64), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("final_stage", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.String(length=32), nullable=True),
        sa.Column("total_frames", sa.Integer(), nullable=True),
        sa.Column("play_duration", sa.Float(), nullable=True),
        sa.Column("enemies_destroyed", sa.Integer(), nullable=True),
        sa.Column("shots_fired", sa.Integer(), nullable=True),
        sa.Column("hits", sa.Integer(), nullable=True),
        sa.Column("deaths", sa.Integer(), nullable=True),
        sa.Column("frames_data", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    # Create indexes
    op.create_index("ix_gameplays_nickname", "gameplays", ["nickname"])
    op.create_index("ix_gameplays_score", "gameplays", ["score"])
    op.create_index("ix_gameplays_model_id", "gameplays", ["model_id"])
    op.create_index("ix_gameplays_created_at", "gameplays", ["created_at"])
    op.create_index("ix_gameplays_score_created", "gameplays", ["score", "created_at"])
    op.create_index("ix_gameplays_model_score", "gameplays", ["model_id", "score"])


def downgrade() -> None:
    # Drop indexes
    op.drop_index("ix_gameplays_model_score", table_name="gameplays")
    op.drop_index("ix_gameplays_score_created", table_name="gameplays")
    op.drop_index("ix_gameplays_created_at", table_name="gameplays")
    op.drop_index("ix_gameplays_model_id", table_name="gameplays")
    op.drop_index("ix_gameplays_score", table_name="gameplays")
    op.drop_index("ix_gameplays_nickname", table_name="gameplays")

    # Drop table
    op.drop_table("gameplays")
