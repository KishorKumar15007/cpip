"""add refresh tokens

Revision ID: b3d01eeac5fa
Revises: 7f98b0ba77c4
Create Date: 2026-08-16 20:11:26.858787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3d01eeac5fa'
down_revision: Union[str, Sequence[str], None] = '7f98b0ba77c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "RefreshTokens",
        sa.Column(
            "refresh_token_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "token_hash",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ['User.user_id'],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("refresh_token_id"),
        sa.UniqueConstraint(
            "token_hash",
            name="uq_refreshtokens_token_hash",
        ),
    )


def downgrade() -> None:
    op.drop_table("RefreshTokens")
