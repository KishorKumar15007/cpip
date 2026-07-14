from datetime import datetime

from sqlalchemy import Text, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class Submission(Base):
    __tablename__ = "Submissions"

    __table_args__ = (
        UniqueConstraint(
            "platform",
            "platform_submission_id",
            name="uq_submission_platform_platform_submission_id",
        ),

        CheckConstraint(
            "attempt_number > 0",
            name="ck_submission_attempt_number_positive",
        ),

        Index(
            "idx_submissions_user_id",
            "user_id",
        ),

        Index(
            "idx_submissions_problem_id",
            "problem_id",
        ),

        Index(
            "idx_submissions_session_id",
            "session_id",
        ),

        Index(
            "idx_submissions_submitted_at",
            "submitted_at",
        ),

        Index(
            "idx_submissions_user_problem",
            "user_id",
            "problem_id",
        ),
    )

    submission_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("User.user_id"),
        nullable=False
    )

    session_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("UserSessions.session_id"),
        nullable=True
    )

    problem_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("Problems.problem_id"),
        nullable=False
    )

    platform: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    platform_submission_id: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    verdict: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    language: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
