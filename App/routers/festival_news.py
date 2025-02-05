from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from App.models import FestivalNews
from App.schemas import FestivalNewsBase, FestivalNewsCreate, FestivalNewsUpdate
from App.database import get_db
from typing import List, Optional
import time 

router = APIRouter()

# POST: Create new festival news
@router.post("/", response_model=FestivalNewsBase)
def create_festival_news(news_data: FestivalNewsCreate, db: Session = Depends(get_db)):
    news = FestivalNews(
        title=news_data.title,
        content=news_data.content,
        created_at=int(time.time())  # Using current Unix timestamp as created_at
    )

    db.add(news)
    db.commit()
    db.refresh(news)

    return news

# GET: Get all festival news
@router.get("/", response_model=List[FestivalNewsBase])
def get_festival_news(db: Session = Depends(get_db)):
    news = db.query(FestivalNews).all()
    
    if not news:
        raise HTTPException(status_code=404, detail="No festival news found")

    return news

# GET: Get specific festival news by ID
@router.get("/{news_id}", response_model=FestivalNewsBase)
def get_festival_news_by_id(news_id: int, db: Session = Depends(get_db)):
    news = db.query(FestivalNews).filter(FestivalNews.id == news_id).first()

    if not news:
        raise HTTPException(status_code=404, detail="Festival news not found")

    return news

# PUT: Update existing festival news
@router.put("/{news_id}", response_model=FestivalNewsBase)
def update_festival_news(news_id: int, news_data: FestivalNewsUpdate, db: Session = Depends(get_db)):
    news = db.query(FestivalNews).filter(FestivalNews.id == news_id).first()

    if not news:
        raise HTTPException(status_code=404, detail="Festival news not found")

    if news_data.title:
        news.title = news_data.title
    if news_data.content:
        news.content = news_data.content

    db.commit()
    db.refresh(news)

    return news

# DELETE: Delete festival news
@router.delete("/{news_id}")
def delete_festival_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(FestivalNews).filter(FestivalNews.id == news_id).first()

    if not news:
        raise HTTPException(status_code=404, detail="Festival news not found")

    db.delete(news)
    db.commit()

    return {"message": "Festival news deleted successfully"}
