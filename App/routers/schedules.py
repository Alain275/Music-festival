from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(database.get_db)):
    return crud.create_schedule(db=db, schedule=schedule)

@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    schedules = crud.get_schedules(db, skip=skip, limit=limit)
    return schedules

@router.get("/{schedule_id}", response_model=schemas.Schedule)
def read_schedule(schedule_id: int, db: Session = Depends(database.get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleUpdate, db: Session = Depends(database.get_db)):
    db_schedule = crud.update_schedule(db, schedule_id=schedule_id, schedule=schedule)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

@router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(database.get_db)):
    db_schedule = crud.delete_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule