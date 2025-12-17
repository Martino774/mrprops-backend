from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Booking
from schemas import BookingCreate, BookingResponse
from dependencies import get_db
from routers.auth import get_current_user

router = APIRouter()

@router.get("/bookings", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@router.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    for key, value in booking.model_dump().items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db.query(Booking).filter(Booking.id == booking_id).delete()
    db.commit()
    return {"message": "Booking deleted"}