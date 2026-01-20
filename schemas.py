from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# Schemas para Properties
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    location: Optional[str] = None
    image_url: Optional[str] = None
    property_type: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[int] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyResponse(PropertyBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# Schemas para Users
class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas para Auth
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Schemas para Bookings
class BookingBase(BaseModel):
    user_id: int
    property_id: int
    start_date: date
    end_date: date
    total_amount: float

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    status: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# Schemas para Payments
class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    status: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
