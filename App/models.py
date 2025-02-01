from sqlalchemy import Column, Boolean,Integer, String, Float, ForeignKey, DateTime,Enum
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Text
from enum import Enum as PyEnum  # Use Python's Enum

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String)
    country = Column(String)
    image_url = Column(String)

    class Config:
        extra = "allow"

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    capacity = Column(Integer)

    class Config:
        extra = "allow"

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    stage_id = Column(Integer, ForeignKey("stages.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    artist = relationship("Artist")
    stage = relationship("Stage")

    class Config:
        extra = "allow"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    class Config:
        extra = "allow"

# Define user roles
class UserRole(str, PyEnum):
    admin = "admin"
    artist = "artist"
    attendee = "attendee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.attendee, nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False)  # One-to-One

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)  # 1-5 stars
    feedback = Column(String, nullable=True)


class FestivalNews(Base):
    __tablename__ = "festival_news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text, index=True)
    created_at = Column(Integer)  # Store as a timestamp (Unix Time)    

    

       