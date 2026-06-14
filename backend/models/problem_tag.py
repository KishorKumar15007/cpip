from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class ProblemTag(Base):
    __tablename__ = "ProblemTags"

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("Problems.problem_id"),
        primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("Tags.tag_id"),
        primary_key=True
    )

    
