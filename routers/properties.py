from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Property
from schemas import PropertyCreate, PropertyResponse
from dependencies import get_db
from routers.auth import get_current_user

router = APIRouter()

@router.get("/properties", response_model=list[PropertyResponse])
def get_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()

@router.get("/properties/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.post("/properties", response_model=PropertyResponse)
def create_property(property: PropertyCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_property = Property(**property.model_dump())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property

@router.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, property: PropertyCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    for key, value in property.model_dump().items():
        setattr(db_property, key, value)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db.query(Property).filter(Property.id == property_id).delete()
    db.commit()
    return {"message": "Property deleted"}