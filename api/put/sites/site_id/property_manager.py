from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class SitePropertyManagerUpdate(BaseModel):
    property_manager: int

@router.put("/sites/{site_id}/property_manager")
async def update_site_property_manager(site_id: int, pm_update: SitePropertyManagerUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    pm = db.query(models.User).filter(models.User.id == pm_update.property_manager).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Property Manager not found")
    if pm.role not in ["property_manager", "admin"]:
        raise HTTPException(status_code=400, detail="User does not have the property_manager or admin role")
        
    db_site.property_manager = pm_update.property_manager
    db.commit()
    db.refresh(db_site)
    return db_site
