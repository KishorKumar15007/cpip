from datetime import datetime

from sqlalchemy import Text, Integer, DateTime, CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class Problem(Base):
    __tablename__ = "Problems"

    __table_args__ = (
        UniqueConstraint(
            "platform",
            "platform_problem_id",
            name="uq_problems_platform_platform_problem_id",
        ),
        CheckConstraint(
            "platform IN ('codeforces', 'leetcode')",
            name="ck_problems_platform",
        ),
        CheckConstraint(
            "cf_rating IS NULL OR cf_rating > 0",
            name="ck_problems_cf_rating_positive",
        ),
    )

    problem_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    platform: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    platform_problem_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    platform_difficulty: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cf_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
