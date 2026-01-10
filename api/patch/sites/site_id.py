from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import Optional, Literal

router = APIRouter()

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_manager: Optional[str] = None
    facility_manager: Optional[str] = None

@router.patch("/sites/{site_id}")
async def update_site(
    site_id: int, 
    site_update: SiteUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    update_data = site_update.dict(exclude_unset=True)
    
    # Validate property_manager if provided
    if "property_manager" in update_data:
        pm = db.query(models.User).filter(models.User.email == update_data["property_manager"]).first()
        if not pm:
            raise HTTPException(status_code=404, detail=f"Property Manager with email {update_data['property_manager']} not found")
        if pm.role != "property_manager":
            raise HTTPException(status_code=400, detail=f"User {update_data['property_manager']} does not have the property_manager role")

    # Validate facility_manager if provided
    if "facility_manager" in update_data:
        fm = db.query(models.User).filter(models.User.email == update_data["facility_manager"]).first()
        if not fm:
            raise HTTPException(status_code=404, detail=f"Facility Manager with email {update_data['facility_manager']} not found")
        if fm.role != "facility_manager":
            raise HTTPException(status_code=400, detail=f"User {update_data['facility_manager']} does not have the facility_manager role")

    for key, value in update_data.items():
        setattr(db_site, key, value)
    
    db.commit()
    db.refresh(db_site)
    
    return {
        "id": str(db_site.id),
        "name": db_site.name,
        "address": db_site.address,
        "latitude": db_site.latitude,
        "longitude": db_site.longitude,
        "property_manager": db_site.property_manager,
        "facility_manager": db_site.facility_manager
    }
