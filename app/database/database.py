from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SQLite database file
DATABASE_PATH = BASE_DIR / "library.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()