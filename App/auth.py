from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import  jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas, crud, database  # Adjust according to your project structure


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create the access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create FastAPI router for authentication endpoints
router = APIRouter()
# Store blacklisted tokens (for demo purposes; use a database in production)
blacklisted_tokens = set()

# Token route for login
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Retrieve the user by username from the database
    user = crud.get_user_by_username(db, username=form_data.username)
    if user is None or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create the access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



blacklisted_tokens = set()

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):  # Correct usage of Depends
    if token in blacklisted_tokens:
        raise HTTPException(status_code=400, detail="Token already invalidated")

    blacklisted_tokens.add(token)
    return {"message": "Successfully logged out"}



