# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# Artist functions
def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()

def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()

def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def update_artist(db: Session, artist_id: int, artist: schemas.ArtistUpdate):
    db_artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()
    if db_artist:
        update_data = artist.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_artist, key, value)
        db.commit()
        db.refresh(db_artist)
    return db_artist

def delete_artist(db: Session, artist_id: int):
    db_artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()
    if db_artist:
        db.delete(db_artist)
        db.commit()
    return db_artist

# Stage functions
def get_stage(db: Session, stage_id: int):
    return db.query(models.Stage).filter(models.Stage.id == stage_id).first()

def get_stages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stage).offset(skip).limit(limit).all()

def create_stage(db: Session, stage: schemas.StageCreate):
    db_stage = models.Stage(**stage.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def update_stage(db: Session, stage_id: int, stage: schemas.StageUpdate):
    db_stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if db_stage:
        update_data = stage.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_stage, key, value)
        db.commit()
        db.refresh(db_stage)
    return db_stage

def delete_stage(db: Session, stage_id: int):
    db_stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if db_stage:
        db.delete(db_stage)
        db.commit()
    return db_stage

# Schedule functions
def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Schedule).offset(skip).limit(limit).all()

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def update_schedule(db: Session, schedule_id: int, schedule: schemas.ScheduleUpdate):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule:
        update_data = schedule.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_schedule, key, value)
        db.commit()
        db.refresh(db_schedule)
    return db_schedule

def delete_schedule(db: Session, schedule_id: int):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
    return db_schedule

# Ticket functions
def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_ticket(db: Session, ticket_id: int, ticket: schemas.TicketUpdate):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        update_data = ticket.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ticket, key, value)
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
    return db_ticket


from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing
def hash_password(password: str):
    return pwd_context.hash(password)

# Get user by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Get users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Create user and auto-create profile
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=hashed_password, role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Automatically create the profile after user creation
    db_profile = models.Profile(user_id=db_user.id, bio="New user profile", image_url=None)
    db.add(db_profile)
    db.commit()

    return db_user

# Update user
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = hash_password(update_data.pop('password'))
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete user
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
