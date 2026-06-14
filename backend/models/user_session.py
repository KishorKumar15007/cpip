from datetime import datetime

from sqlalchemy import DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class UserSession(Base):
    __tablename__ = "UserSessions"

    __table_args__ = (
        CheckConstraint(
            "ended_at > started_at",
            name="ck_usersessions_valid_time_range",
        ),
    )

    session_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.user_id"),
        nullable=False
    )
    
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    ended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
