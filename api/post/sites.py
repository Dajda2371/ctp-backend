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
    coordinator: Literal["admin", "property_manager", "facility_manager"]

@router.post("/sites")
async def create_site(site: SiteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_site = models.Site(
        name=site.name,
        address=site.address,
        latitude=site.latitude,
        longitude=site.longitude,
        coordinator=site.coordinator
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
        "coordinator": new_site.coordinator
    }
