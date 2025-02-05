from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Ticket)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    return crud.create_ticket(db=db, ticket=ticket)

@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def read_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(database.get_db)):
    # db_ticket = crud.update_ticket(db, ticket_id=ticket_id, ticket=ticket)
    db_ticket = crud.update_ticket(db, ticket_id=ticket_id, ticket_update=ticket)

    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.delete("/{ticket_id}", response_model=schemas.Ticket)
def delete_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    db_ticket = crud.delete_ticket(db, ticket_id=ticket_id)
    
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket