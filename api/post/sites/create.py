from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import Literal

router = APIRouter()

class SiteCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    property_manager: str  # Email
    facility_manager: str  # Email

@router.post("/sites")
async def create_site(site: SiteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Validate property_manager exists and has the correct role
    pm = db.query(models.User).filter(models.User.email == site.property_manager).first()
    if not pm:
        raise HTTPException(status_code=404, detail=f"Property Manager with email {site.property_manager} not found")
    if pm.role not in ["property_manager", "admin"]:
        raise HTTPException(status_code=400, detail=f"User {site.property_manager} does not have the property_manager or admin role")

    # Validate facility_manager exists and has the correct role
    fm = db.query(models.User).filter(models.User.email == site.facility_manager).first()
    if not fm:
        raise HTTPException(status_code=404, detail=f"Facility Manager with email {site.facility_manager} not found")
    if fm.role not in ["facility_manager", "admin"]:
        raise HTTPException(status_code=400, detail=f"User {site.facility_manager} does not have the facility_manager or admin role")

    new_site = models.Site(
        name=site.name,
        address=site.address,
        latitude=site.latitude,
        longitude=site.longitude,
        property_manager=site.property_manager,
        facility_manager=site.facility_manager
    )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return {
        "id": str(new_site.id),
        "name": new_site.name,
        "address": new_site.address,
        "latitude": new_site.latitude,
        "longitude": new_site.longitude,
        "property_manager": new_site.property_manager,
        "facility_manager": new_site.facility_manager
    }
