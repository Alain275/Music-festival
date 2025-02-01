from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

# Database URL for SQLite (replace with your actual database URL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class to handle the session with the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency that provides a DB session to FastAPI route handlers
def get_db() -> Session:
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session to FastAPI
    finally:
        db.close()  # Close the session when done





