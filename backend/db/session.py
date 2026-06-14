from sqlalchemy.orm import sessionmaker

from backend.db.connection import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
