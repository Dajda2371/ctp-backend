from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class SiteAddressUpdate(BaseModel):
    address: str

@router.put("/sites/{site_id}/address")
async def update_site_address(site_id: int, address_update: SiteAddressUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.address = address_update.address
    db.commit()
    db.refresh(db_site)
    return db_site
