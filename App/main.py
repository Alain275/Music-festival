from fastapi import FastAPI, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import artists, stages, schedules, tickets, users,rating
# from .config import MTN_API_URL, CLIENT_ID, CLIENT_SECRET, SHORTCODE
import requests
from . import models
from .database import engine
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import text
from App.routers import rating, festival_news,profiles # Assuming this is your path structure
from . import auth
import os


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi import FastAPI, HTTPException
import os
import requests
from dotenv import load_dotenv

# # Load environment variables from the .env file
# load_dotenv()

app = FastAPI()

# PayPal Credentials from environment variables
PAYPAL_CLIENT_ID = "AaAYMuTPFNWE7PdlmTNFY7KgvX-uWkyZiFQnXSbzyyYqE-Ee-dMM_Jz_O3MQpqDuF81FqkAtV8xMcwYs" 
PAYPAL_CLIENT_SECRET = "ECaDbhv4EriqkBZy2ZdKoHX4UDGJv-_KYiOs5q_N3bfw2_6S1Nw_oOKeyz_GYgFtHeUs1tg_Xolwfrdh"  # Use actual environment variable for PayPal client secret
PAYPAL_API_URL = "https://api.sandbox.paypal.com/v2/checkout/orders"

import requests
from fastapi import FastAPI, HTTPException
import warnings

app = FastAPI()
warnings.filterwarnings("ignore", category=UserWarning, message="Valid config keys have changed in V2")

# Hardcoded PayPal Credentials (for testing only)
PAYPAL_CLIENT_ID = "AaAYMuTPFNWE7PdlmTNFY7KgvX-uWkyZiFQnXSbzyyYqE-Ee-dMM_Jz_O3MQpqDuF81FqkAtV8xMcwYs"
PAYPAL_CLIENT_SECRET = "ECaDbhv4EriqkBZy2ZdKoHX4UDGJv-_KYiOs5q_N3bfw2_6S1Nw_oOKeyz_GYgFtHeUs1tg_Xolwfrdh"

# PayPal API URLs
PAYPAL_AUTH_URL = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
PAYPAL_ORDER_URL = "https://api-m.sandbox.paypal.com/v2/checkout/orders"

# Function to get the PayPal access token
def get_paypal_access_token():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(PAYPAL_AUTH_URL, headers=headers, data=data, auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET))

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("🔑 Access Token:", access_token)  # Print for debugging
        return access_token
    else:
        print("❌ PayPal Token Error:", response.status_code, response.text)
        raise HTTPException(status_code=400, detail="Unable to retrieve PayPal access token")


# Endpoint to create a payment order
@app.post("/create_payment_order")
async def create_payment_order(amount: float, currency: str = "USD"):
    print(f"Received Currency: {currency}")  # Debugging
    access_token = get_paypal_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": currency.upper(),
                "value": str(amount)
            }
        }],
        "application_context": {
            "return_url": "http://localhost:8000/execute_payment",
            "cancel_url": "http://localhost:8000/cancel_payment"
        }
    }

    response = requests.post(PAYPAL_ORDER_URL, json=order_data, headers=headers)

    if response.status_code == 201:
        order = response.json()
        approve_url = next((link["href"] for link in order["links"] if link["rel"] == "approve"), None)
        
        print(" Order Created:", order)  # Print full order details
        return {
            "order_id": order["id"],
            "approve_url": approve_url or "Approval URL not found"
        }
    else:
        print(" PayPal Order Error:", response.status_code, response.text)
        raise HTTPException(status_code=400, detail=f"Error creating payment order: {response.text}")

limiter = Limiter(key_func=get_remote_address)

from sqlalchemy import text

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Ensure this uses `text()`
        
        return {"status": "healthy", "database": "connected"}
    
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(artists.router, prefix="/artists", tags=["artists"])
app.include_router(stages.router, prefix="/stages", tags=["stages"])
app.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
app.include_router(rating.router, prefix="/rating", tags=["rating"])
app.include_router(rating.router, prefix="/rating", tags=["rating"])
app.include_router(festival_news.router, prefix="/festival_news", tags=["festival_news"])  # Include the festival news routes


@app.get("/")
async def root():
    return {"message": "Welcome to the Music Festival Management API"}

# If you still want to log requests and responses, you can use FastAPI's middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"Request: {request.method} {request.url}")
    print(f"Response Status: {response.status_code}")
    return response
