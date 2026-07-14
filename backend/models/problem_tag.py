from sqlalchemy import ForeignKey, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class ProblemTag(Base):
    __tablename__ = "ProblemTags"

    __table_args__ = (
        Index(
            "idx_problemtags_problem_id",
            "problem_id",
        ),

        Index(
            "idx_problemtags_tag_id",
            "tag_id",
        ),
    )

    problem_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("Problems.problem_id"),
        primary_key=True,
    )

    tag_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("Tags.tag_id"),
        primary_key=True,
    )
