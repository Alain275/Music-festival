from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

async def setup_cache():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Use the cache decorator in your endpoints
@router.get("/artists/", response_model=List[schemas.Artist])
@cache(expire=60)
async def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    artists = crud.get_artists(db, skip=skip, limit=limit)
    return artists