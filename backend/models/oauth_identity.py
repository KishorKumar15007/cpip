from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Identity,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class OAuthIdentity(Base):
    __tablename__ = "OAuthIdentities"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_id",
            name="uq_oauthidentities_provider_provider_id",
        ),
        UniqueConstraint(
            "user_id",
            "provider",
            name="uq_oauthidentities_user_provider",
        ),
        CheckConstraint(
            "provider IN ('google', 'github')",
            name="ck_oauthidentities_provider",
        ),
    )

    identity_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "User.user_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    provider_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
