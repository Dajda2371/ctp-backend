from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class SiteLatitudeUpdate(BaseModel):
    latitude: float

@router.put("/sites/{site_id}/latitude")
async def update_site_latitude(site_id: int, lat_update: SiteLatitudeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.latitude = lat_update.latitude
    db.commit()
    db.refresh(db_site)
    return db_site
