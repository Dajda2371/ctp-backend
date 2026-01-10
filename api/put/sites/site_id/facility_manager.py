from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class SiteFacilityManagerUpdate(BaseModel):
    facility_manager: str

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
