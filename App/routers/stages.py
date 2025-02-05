from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Stage)
def create_stage(stage: schemas.StageCreate, db: Session = Depends(database.get_db)):
    return crud.create_stage(db=db, stage=stage)

@router.get("/", response_model=List[schemas.Stage])
def read_stages(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    stages = crud.get_stages(db, skip=skip, limit=limit)
    return stages

@router.get("/{stage_id}", response_model=schemas.Stage)
def read_stage(stage_id: int, db: Session = Depends(database.get_db)):
    db_stage = crud.get_stage(db, stage_id=stage_id)
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    return db_stage

@router.put("/{stage_id}", response_model=schemas.Stage)
def update_stage(stage_id: int, stage: schemas.StageUpdate, db: Session = Depends(database.get_db)):
    db_stage = crud.update_stage(db, stage_id=stage_id, stage=stage)
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    return db_stage

@router.delete("/{stage_id}", response_model=schemas.Stage)
def delete_stage(stage_id: int, db: Session = Depends(database.get_db)):
    db_stage = crud.delete_stage(db, stage_id=stage_id)
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    return db_stage
