from sqlalchemy import Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class Tag(Base):
    __tablename__ = "Tags"

    tag_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    
    name: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )
