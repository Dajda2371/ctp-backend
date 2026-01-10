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
    property_manager: Optional[int] = None
    facility_manager: Optional[int] = None

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
        pm = db.query(models.User).filter(models.User.id == update_data["property_manager"]).first()
        if not pm:
            raise HTTPException(status_code=404, detail=f'Property Manager with ID "{update_data["property_manager"]}" not found')
        if pm.role not in ["property_manager", "admin"]:
            raise HTTPException(status_code=400, detail=f'User with ID "{update_data["property_manager"]}" does not have the property_manager or admin role')

    # Validate facility_manager if provided
    if "facility_manager" in update_data:
        fm = db.query(models.User).filter(models.User.id == update_data["facility_manager"]).first()
        if not fm:
            raise HTTPException(status_code=404, detail=f'Facility Manager with ID "{update_data["facility_manager"]}" not found')
        if fm.role not in ["facility_manager", "admin"]:
            raise HTTPException(status_code=400, detail=f'User with ID "{update_data["facility_manager"]}" does not have the facility_manager or admin role')

    for key, value in update_data.items():
        setattr(db_site, key, value)
    
    db.commit()
    
    from sqlalchemy.orm import aliased
    PM = aliased(models.User)
    FM = aliased(models.User)
    
    result = db.query(
        models.Site,
        PM.name.label("pm_name"),
        FM.name.label("fm_name")
    ).outerjoin(PM, models.Site.property_manager == PM.id)\
     .outerjoin(FM, models.Site.facility_manager == FM.id)\
     .filter(models.Site.id == site_id).first()
     
    site, pm_name, fm_name = result
    
    return {
        "id": site.id,
        "name": site.name,
        "address": site.address,
        "latitude": site.latitude,
        "longitude": site.longitude,
        "property_manager": site.property_manager,
        "property_manager_name": pm_name,
        "facility_manager": site.facility_manager,
        "facility_manager_name": fm_name
    }
