
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from .ml_logic import predict_booking_probability
import random

app = FastAPI(title="Sleeper Bus Ticket Booking System")

# --- Mock Data Models ---

class Seat(BaseModel):
    seat_id: str
    type: str = "Sleeper"  # 'Upper', 'Lower'
    price: int = 800
    is_booked: bool = False
    booked_by: Optional[str] = None
    meal: Optional[str] = None # 'Veg', 'Non-Veg', 'None'

class BookingRequest(BaseModel):
    seat_id: str
    user_name: str
    meal: Optional[str] = "None"

class CancelRequest(BaseModel):
    seat_id: str
    user_name: str # meaningful for validation in real app

class ProbabilityRequest(BaseModel):
    days_prior: int
    seat_type: str
    is_weekend: bool

class Station(BaseModel):
    name: str
    arrival_time: str

# --- In-Memory Database ---

# Mock 20 Sleeper Seats (10 Lower, 10 Upper)
SEATS_DB: Dict[str, Seat] = {}

def init_db():
    rows = 5
    # Lower Berths (L1-L5, R1-R5) - simplified to 1-10 for demo
    for i in range(1, 11):
        seat_id = f"L{i}"
        SEATS_DB[seat_id] = Seat(seat_id=seat_id, type="Lower Sleeper", price=800)
    
    # Upper Berths
    for i in range(1, 11):
        seat_id = f"U{i}"
        SEATS_DB[seat_id] = Seat(seat_id=seat_id, type="Upper Sleeper", price=700)

init_db()

STATIONS_DB = [
    Station(name="Ahmedabad (Start)", arrival_time="10:00 PM"),
    Station(name="Vadodara", arrival_time="11:30 PM"),
    Station(name="Surat", arrival_time="02:00 AM"),
    Station(name="Vapi", arrival_time="04:00 AM"),
    Station(name="Mumbai (End)", arrival_time="07:00 AM")
]

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to Sleeper Bus API"}

@app.get("/seats", response_model=List[Seat])
def get_seats():
    return list(SEATS_DB.values())

@app.post("/book-seat")
def book_seat(booking: BookingRequest):
    seat_id = booking.seat_id
    if seat_id not in SEATS_DB:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    seat = SEATS_DB[seat_id]
    if seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat already booked")
    
    # Update DB
    seat.is_booked = True
    seat.booked_by = booking.user_name
    seat.meal = booking.meal
    
    return {"status": "confirmed", "seat": seat, "message": "Booking successful!"}

@app.post("/book-meal")
def book_meal(seat_id: str, meal: str):
    if seat_id not in SEATS_DB:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    seat = SEATS_DB[seat_id]
    if not seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat mock booked yet")
        
    seat.meal = meal
    return {"status": "updated", "meal": meal}

@app.post("/cancel-booking")
def cancel_booking(request: CancelRequest):
    seat_id = request.seat_id
    if seat_id not in SEATS_DB:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    seat = SEATS_DB[seat_id]
    if not seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat is not currently booked")
    
    # Mock validation: Check if user matches (skipped for loose prototype)
    
    # Reset Seat
    seat.is_booked = False
    seat.booked_by = None
    seat.meal = None
    
    return {"status": "cancelled", "message": "Booking cancelled successfully"}

@app.get("/stations", response_model=List[Station])
def get_stations():
    return STATIONS_DB

@app.post("/predict-probability")
def predict_probability(request: ProbabilityRequest):
    prob = predict_booking_probability(request.days_prior, request.seat_type, request.is_weekend)
    return {
        "confirmation_probability": prob, 
        "analysis": "High chance" if prob > 70 else "Medium chance" if prob > 40 else "Low chance"
    }

