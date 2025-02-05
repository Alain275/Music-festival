from fastapi import APIRouter
from slowapi.util import get_remote_address
from slowapi import Limiter
from sqlalchemy import text
from ..database import engine

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/")
async def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Ensure this uses `text()`
        
        return {"status": "healthy", "database": "connected"}
    
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
