"""drop consent artifacts

Revision ID: 96a09501951b
Revises: 45908820146f
Create Date: 2025-09-09 17:23:53.632421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "96a09501951b"
down_revision: Union[str, None] = "45908820146f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop consents table if exists
    try:
        op.drop_table("consents")
    except Exception:
        # table may not exist if never applied
        pass
    # Drop participant consent columns if exist
    with op.batch_alter_table("participants") as bop:
        try:
            bop.drop_column("consent_version")
        except Exception:
            pass
        try:
            bop.drop_column("consent_accepted_at")
        except Exception:
            pass


def downgrade() -> None:
    # Recreate dropped columns and table (best-effort)
    with op.batch_alter_table("participants") as bop:
        bop.add_column(
            sa.Column("consent_version", sa.String(length=32), nullable=True)
        )
        bop.add_column(
            sa.Column("consent_accepted_at", sa.DateTime(timezone=True), nullable=True)
        )
    op.create_table(
        "consents",
        sa.Column("version", sa.String(length=32), primary_key=True),
        sa.Column("document_url", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
