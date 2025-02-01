
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


# Artist schemas
class ArtistBase(BaseModel):
    name: str = Field(..., example="The Beatles", min_length=1, max_length=100)
    genre: str = Field(..., example="Rock", min_length=1, max_length=50)
    country: str = Field(..., example="United Kingdom", min_length=1, max_length=100)
    image_url: Optional[str] = Field(None, example="https://example.com/beatles.jpg")

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    name: Optional[str] = Field(None, example="The Rolling Stones", min_length=1, max_length=100)
    genre: Optional[str] = Field(None, example="Rock", min_length=1, max_length=50)
    country: Optional[str] = Field(None, example="United Kingdom", min_length=1, max_length=100)
    image_url: Optional[str] = Field(None, example="https://example.com/rollingstones.jpg")

class Artist(ArtistBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True  # Instead of orm_mode
        populate_by_name = True  # Instead of allow_population_by_field_name


# Stage schemas
class StageBase(BaseModel):
    name: str = Field(..., example="Main Stage", min_length=1, max_length=100)
    location: str = Field(..., example="Central Park", min_length=1, max_length=200)
    capacity: int = Field(..., example=5000, gt=0)

class StageCreate(StageBase):
    pass

class StageUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Secondary Stage", min_length=1, max_length=100)
    location: Optional[str] = Field(None, example="Riverside", min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, example=3000, gt=0)

class Stage(StageBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        populate_by_name = True


# Schedule schemas
class ScheduleBase(BaseModel):
    artist_id: int = Field(..., example=1, gt=0)
    stage_id: int = Field(..., example=1, gt=0)
    start_time: datetime = Field(..., example="2023-07-15T20:00:00")
    end_time: datetime = Field(..., example="2023-07-15T22:00:00")

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    artist_id: Optional[int] = Field(None, example=2, gt=0)
    stage_id: Optional[int] = Field(None, example=2, gt=0)
    start_time: Optional[datetime] = Field(None, example="2023-07-15T21:00:00")
    end_time: Optional[datetime] = Field(None, example="2023-07-15T23:00:00")

class Schedule(ScheduleBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        populate_by_name = True


# Ticket schemas
class TicketBase(BaseModel):
    type: str = Field(..., example="VIP", min_length=1, max_length=50)
    price: float = Field(..., example=150.00, ge=0)
    quantity: int = Field(..., example=100, ge=0)

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    type: Optional[str] = Field(None, example="Regular", min_length=1, max_length=50)
    price: Optional[float] = Field(None, example=75.00, ge=0)
    quantity: Optional[int] = Field(None, example=500, ge=0)

class Ticket(TicketBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        populate_by_name = True


# User schemas
class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

class UserCreate(UserBase):
    password: str = Field(..., example="strongpassword123", min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="newuser@example.com")
    password: Optional[str] = Field(None, example="newstrongpassword123", min_length=8)
    is_active: Optional[bool] = Field(None, example=True)
    is_admin: Optional[bool] = Field(None, example=False)

class User(UserBase):
    id: int = Field(..., example=1)
    is_active: bool = Field(..., example=True)
    is_admin: bool = Field(..., example=False)

    class Config:
        from_attributes = True
        populate_by_name = True



class RatingBase(BaseModel):
    id: int
    artist_id: int
    score: int
    feedback: Optional[str] = None  # Include feedback in the base schema

    class Config:
   
        from_attributes = True

class RatingCreate(BaseModel):
    artist_id: int
    score: int
    feedback: Optional[str] = None  # Include feedback in the creation schema


class RatingUpdate(BaseModel):  # Define this since it was referenced but missing
    score: Optional[int] = None




from pydantic import BaseModel
from typing import Optional

# Define a schema for OAuth2 login request
class OAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str

# Define a schema for the Token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Define a schema for the TokenData (the data embedded in the JWT token)
class TokenData(BaseModel):
    username: str

# Define user roles
class UserRole(str, Enum):
    admin = "admin"
    artist = "artist"
    attendee = "attendee"

# Base schema for User (shared fields)
class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: Optional[str] = None 
    role: UserRole

# Schema for creating a user
class UserCreate(UserBase):
    password: str  # Required for new users

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

# Schema for returning user data
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# Profile schema
class ProfileBase(BaseModel):
    bio: Optional[str] = None
    image_url: Optional[str] = None
    user: Optional[UserBase]  # Include user details

class ProfileCreate(ProfileBase):
    username: str
    email: str
    password: str  
    role: Optional[UserRole] = UserRole.attendee

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class FestivalNewsBase(BaseModel):
    title: str
    content: str

    class Config:
   
        from_attributes = True

class FestivalNewsCreate(FestivalNewsBase):
    pass

class FestivalNewsUpdate(FestivalNewsBase):
    title: Optional[str] = None
    content: Optional[str] = None        





