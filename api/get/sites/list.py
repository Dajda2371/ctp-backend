from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/sites")
async def get_sites(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sites = db.query(models.Site).all()
    return [
        {
            "id": str(site.id),
            "name": site.name,
            "address": site.address,
            "latitude": site.latitude,
            "longitude": site.longitude,
            "property_manager": site.property_manager,
            "facility_manager": site.facility_manager
        } for site in sites
    ]
