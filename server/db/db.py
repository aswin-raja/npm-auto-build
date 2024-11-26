from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Define the SQLite database file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "auto_build.db")

# Construct DATABASE_URL for SQLite
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=True, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
