from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import Optional

router = APIRouter()

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    coordinator: Optional[str] = None

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
    for key, value in update_data.items():
        setattr(db_site, key, value)
    
    db.commit()
    db.refresh(db_site)
    
    return {
        "id": str(db_site.id),
        "name": db_site.name,
        "address": db_site.address,
        "coordinator": db_site.coordinator
    }
