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

class SiteCoordinatorUpdate(BaseModel):
    coordinator: Optional[Literal["admin", "property_manager", "facility_manager"]] = None

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

@router.put("/sites/{site_id}/coordinator")
async def update_site_coordinator(site_id: int, coordinator_update: SiteCoordinatorUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.coordinator = coordinator_update.coordinator
    db.commit()
    db.refresh(db_site)
    return db_site
