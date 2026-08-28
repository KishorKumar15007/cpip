from datetime import datetime

from sqlalchemy import Text, Integer, DateTime, ForeignKey, UniqueConstraint, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class ContestParticipation(Base):
    __tablename__ = "ContestParticipation"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "platform",
            "contest_id",
            name="uq_contestparticipation_user_id_platform_contest_id",
        ),

        Index(
            "idx_contestparticipation_user_id",
            "user_id",
        ),

        Index(
            "idx_contestparticipation_user_date",
            "user_id",
            "participated_at",
        ),
    )

    participation_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("User.user_id"),
        nullable=False
    )

    platform: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    contest_id: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    contest_name: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    old_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    new_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    participated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
