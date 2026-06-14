from datetime import datetime

from sqlalchemy import Text, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class ContestParticipation(Base):
    __tablename__ = "ContestParticipation"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "platform",
            "contest_id",
            name="uq_contestparticipation_user_id_platform_contest_id"
        ),
    )

    participation_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
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


