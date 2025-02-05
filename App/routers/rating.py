from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from App.models import Rating
from App.schemas import RatingBase, RatingCreate, RatingUpdate
from App.database import get_db
from typing import List, Optional

router = APIRouter()

# Define automatic feedback logic based on rating score
def generate_feedback(score: int) -> str:
    if score >= 4:
        return "Great! Thanks for the positive rating. You're a big fan!"
    elif score >= 2:
        return "Thanks for your rating! We’ll strive to do better next time."
    else:
        return "Sorry to hear that! We’ll try to improve next time."
from sqlalchemy.exc import SQLAlchemyError

@router.post("/artists/{artist_id}/rate", response_model=RatingBase)
def rate_artist(artist_id: int, rating_data: RatingCreate, db: Session = Depends(get_db)):
    try:
        feedback = generate_feedback(rating_data.score)
        rating = Rating(
            artist_id=artist_id,
            score=rating_data.score,
            feedback=feedback
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")
    return rating

# GET: Get all ratings for a specific artist, with sorting and filtering
@router.get("/artists/{artist_id}/ratings", response_model=List[RatingBase])
def get_ratings(
    artist_id: int, 
    db: Session = Depends(get_db),
    min_score: Optional[int] = None,
    max_score: Optional[int] = None,
    sort_by: Optional[str] = "score",
    order: Optional[str] = "desc",
):
    query = db.query(Rating).filter(Rating.artist_id == artist_id)
    
    if min_score is not None:
        query = query.filter(Rating.score >= min_score)
    if max_score is not None:
        query = query.filter(Rating.score <= max_score)
    
    if sort_by == "score":
        query = query.order_by(asc(Rating.score) if order == "asc" else desc(Rating.score))
    elif sort_by == "feedback":
        query = query.order_by(asc(Rating.feedback) if order == "asc" else desc(Rating.feedback))
    
    ratings = query.all()
    if not ratings:
        raise HTTPException(status_code=404, detail="Ratings not found")

    return ratings

# PUT: Update an existing rating
@router.put("/artists/{artist_id}/ratings/{rating_id}", response_model=RatingBase)
def update_rating(
    artist_id: int, 
    rating_id: int, 
    rating_data: RatingUpdate, 
    db: Session = Depends(get_db)
):
    rating = db.query(Rating).filter(Rating.id == rating_id, Rating.artist_id == artist_id).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    if rating_data.score is not None:
        rating.score = rating_data.score
        rating.feedback = generate_feedback(rating_data.score)  # Update feedback
    # Uncomment below if you want to allow comment updates as well
    # if rating_data.comment is not None:
    #     rating.comment = rating_data.comment

    db.commit()
    db.refresh(rating)

    return rating

# DELETE: Delete a rating for an artist
@router.delete("/{artist_id}/ratings/{rating_id}")
def delete_rating(artist_id: int, rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id, Rating.artist_id == artist_id).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating)
    db.commit()
    
    return {"message": "Rating deleted successfully"}

# GET: Get a specific rating for an artist
@router.get("/{artist_id}/ratings/{rating_id}", response_model=RatingBase)
def get_rating(artist_id: int, rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id, Rating.artist_id == artist_id).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    return rating



