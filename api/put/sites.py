from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import Optional, Literal

router = APIRouter()

class SiteNameUpdate(BaseModel):
    name: str

class SiteAddressUpdate(BaseModel):
    address: str

class SitePropertyManagerUpdate(BaseModel):
    property_manager: str

class SiteFacilityManagerUpdate(BaseModel):
    facility_manager: str

class SiteLatitudeUpdate(BaseModel):
    latitude: float

class SiteLongitudeUpdate(BaseModel):
    longitude: float

@router.put("/sites/{site_id}/name")
async def update_site_name(site_id: int, name_update: SiteNameUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.name = name_update.name
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/sites/{site_id}/address")
async def update_site_address(site_id: int, address_update: SiteAddressUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.address = address_update.address
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/sites/{site_id}/property_manager")
async def update_site_property_manager(site_id: int, pm_update: SitePropertyManagerUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    pm = db.query(models.User).filter(models.User.email == pm_update.property_manager).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Property Manager not found")
    if pm.role != "property_manager":
        raise HTTPException(status_code=400, detail="User does not have the property_manager role")
        
    db_site.property_manager = pm_update.property_manager
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/sites/{site_id}/facility_manager")
async def update_site_facility_manager(site_id: int, fm_update: SiteFacilityManagerUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")

    fm = db.query(models.User).filter(models.User.email == fm_update.facility_manager).first()
    if not fm:
        raise HTTPException(status_code=404, detail="Facility Manager not found")
    if fm.role != "facility_manager":
        raise HTTPException(status_code=400, detail="User does not have the facility_manager role")

    db_site.facility_manager = fm_update.facility_manager
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/sites/{site_id}/latitude")
async def update_site_latitude(site_id: int, lat_update: SiteLatitudeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.latitude = lat_update.latitude
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/sites/{site_id}/longitude")
async def update_site_longitude(site_id: int, lon_update: SiteLongitudeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.longitude = lon_update.longitude
    db.commit()
    db.refresh(db_site)
    return db_site
