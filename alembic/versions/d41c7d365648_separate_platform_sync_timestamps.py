"""separate platform sync timestamps

Revision ID: d41c7d365648
Revises: b3d01eeac5fa
Create Date: 2026-08-16 20:54:51.310844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd41c7d365648'
down_revision: Union[str, Sequence[str], None] = 'b3d01eeac5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "User",
        sa.Column(
            "cf_last_synced_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "User",
        sa.Column(
            "lc_last_synced_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.drop_column(
        "User",
        "last_synced_at",
    )


def downgrade() -> None:
    op.add_column(
        "User",
        sa.Column(
            "last_synced_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.drop_column(
        "User",
        "cf_last_synced_at",
    )

    op.drop_column(
        "User",
        "lc_last_synced_at",
    )
