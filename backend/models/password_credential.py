from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class PasswordCredential(Base):
    __tablename__ = "PasswordCredentials"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "User.user_id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
