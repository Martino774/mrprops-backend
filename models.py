from sqlalchemy import Column, Integer, String, Float, Text, Enum, Date, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship
from database import Base
import enum

class PropertyType(enum.Enum):
    alquiler = "alquiler"
    venta = "venta"

class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class PaymentStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150))
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(50))
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    bookings = relationship("Booking", back_populates="user")


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    price = Column(DECIMAL(10,2))
    location = Column(String(200))
    image_url = Column(String(500))
    property_type = Column(Enum(PropertyType))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    bookings = relationship("Booking", back_populates="property")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    total_amount = Column(DECIMAL(10,2))
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    amount = Column(DECIMAL(10,2))
    payment_method = Column(String(50))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    booking = relationship("Booking", back_populates="payment")
