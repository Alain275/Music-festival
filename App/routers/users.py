from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter()

# Create user with role
@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Get all users
@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

# Get user by ID
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update user
@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete user
@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
