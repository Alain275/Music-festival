from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from typing import List


router = APIRouter()

@router.post("/", response_model=schemas.Artist)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(database.get_db)):
    return crud.create_artist(db=db, artist=artist)

@router.get("/", response_model=List[schemas.Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    artists = crud.get_artists(db, skip=skip, limit=limit)
    return artists

@router.get("/{artist_id}", response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session = Depends(database.get_db)):
    db_artist = crud.get_artist(db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.put("/{artist_id}", response_model=schemas.Artist)
def update_artist(artist_id: int, artist: schemas.ArtistUpdate, db: Session = Depends(database.get_db)):
    db_artist = crud.update_artist(db, artist_id=artist_id, artist=artist)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.delete("/{artist_id}", response_model=schemas.Artist)
def delete_artist(artist_id: int, db: Session = Depends(database.get_db)):
    db_artist = crud.delete_artist(db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist