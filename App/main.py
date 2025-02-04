import requests
import os
import warnings
from fastapi import FastAPI, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi.util import get_remote_address
from slowapi import Limiter
from sqlalchemy import text
from dotenv import load_dotenv
from .routers import artists, stages, schedules, tickets, users,rating,festival_news,profiles
from .database import engine
from . import models
from . import auth


import os
import requests
import warnings
from datetime import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update
from App.database import engine, get_db
from App.models import Base, Order, Ticket
from App.schemas import OrderCreate  # Schema for order creation
from fastapi.responses import RedirectResponse











app = FastAPI()


models.Base.metadata.create_all(bind=engine)



# Create database tables
Base.metadata.create_all(bind=engine)

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Valid config keys have changed in V2")

# PayPal API Credentials
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_IDS")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRETS")

# PayPal API URLs
PAYPAL_AUTH_URL = os.getenv("PAYPAL_AUTH_URLS")
PAYPAL_ORDER_URL = os.getenv("PAYPAL_ORDER_URLS")
PAYPAL_CAPTURE_URL = "https://api.sandbox.paypal.com/v2/checkout/orders/{}/capture"
PAYPAL_API_URL = "https://api.sandbox.paypal.com/v2/checkout/orders"

app = FastAPI()

# Function to get PayPal access token
def get_paypal_access_token():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(PAYPAL_AUTH_URL, headers=headers, data=data, auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET))

    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="PayPal response missing access_token")

        print(f"🔑 PayPal Access Token: {access_token}")  # Debugging
        return access_token
    else:
        print(f"❌ PayPal Token Error [{response.status_code}]: {response.text}")
        raise HTTPException(status_code=400, detail="Unable to retrieve PayPal access token")




@app.post("/create_order")
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """
    Creates an order in the database and initiates PayPal payment.
    """
    # Validate ticket availability
    ticket = db.query(Ticket).filter(Ticket.id == order_data.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if order_data.quantity > ticket.total_tickets:
        raise HTTPException(status_code=400, detail="Not enough tickets available")

    # Calculate total price
    total_price = order_data.quantity * ticket.price

    # Create order in database (status = PENDING)
    new_order = Order(
        user_id=order_data.user_id,
        ticket_id=order_data.ticket_id,
        quantity=order_data.quantity,
        total_price=total_price,
        status="pending",
        created_at=datetime.utcnow(),
        order_id=None  # Initialize without PayPal order_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Generate PayPal order
    access_token = get_paypal_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    order_payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": f"{total_price:.2f}"
            },
            "description": f"Ticket Order #{new_order.id} - {ticket.type}"
        }],
        "application_context": {
            "return_url": f"http://localhost:8000/execute_payment?order_id={new_order.id}",
            "cancel_url": f"http://localhost:8000/cancel_payment?order_id={new_order.id}"
        }
    }

    response = requests.post(PAYPAL_ORDER_URL, json=order_payload, headers=headers)

    if response.status_code == 201:
        paypal_order = response.json()
        paypal_order_id = paypal_order.get("id")
        approve_url = next((link["href"] for link in paypal_order.get("links", []) if link.get("rel") == "approve"), None)

        if not paypal_order_id or not approve_url:
            raise HTTPException(status_code=400, detail="Missing PayPal order ID or approval URL")

        # Store PayPal order ID in the database
        new_order.order_id = paypal_order_id
        db.commit()

        print(f"✅ PayPal Order Created: {paypal_order_id}")

        # Redirect the user to the PayPal approval URL
        return RedirectResponse(url=approve_url)  # This redirects the user to PayPal for approval
    else:
        print(f"❌ PayPal Order Error [{response.status_code}]: {response.text}")
        raise HTTPException(status_code=400, detail=f"Error creating PayPal order: {response.text}")


# GET endpoint to execute payment and capture funds
@app.get("/execute_payment")
async def execute_payment(order_id: int, db: Session = Depends(get_db)):
    """
    Captures PayPal payment and updates the order status.
    """
    print(f"🔄 Capturing Payment for Order: {order_id}")

    # Get order from database using the database order ID
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Order is not in a pending state")

    # Capture PayPal payment using the paypal_order_id (not the database order_id)
    paypal_order_id = order.order_id  # This is the PayPal order_id string
    capture_url = PAYPAL_CAPTURE_URL.format(paypal_order_id)  # Use the PayPal order_id here

    access_token = get_paypal_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(capture_url, headers=headers)

    if response.status_code == 201:
        capture_data = response.json()
        status = capture_data.get("status", "FAILED")

        # Update order status in database
        order.status = status.lower()
        db.commit()

        # If payment is successful, reduce available ticket count
        if status.lower() == "completed":
            ticket = db.query(Ticket).filter(Ticket.id == order.ticket_id).first()
            if ticket:
                ticket.total_tickets -= order.quantity
                db.commit()

        print(f"✅ Payment Captured: {status}")
        return {"order_id": order.id, "status": status}  # Return the order ID as integer
    else:
        print(f"❌ Payment Capture Error [{response.status_code}]: {response.text}")
        raise HTTPException(status_code=400, detail=f"Error capturing payment: {response.text}")



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
