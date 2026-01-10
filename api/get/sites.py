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
            "coordinator": site.coordinator
        } for site in sites
    ]

@router.get("/sites/{site_id}")
async def get_site(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {
        "id": str(site.id),
        "name": site.name,
        "address": site.address,
        "latitude": site.latitude,
        "longitude": site.longitude,
        "coordinator": site.coordinator
    }

@router.get("/sites/{site_id}/latitude")
async def get_site_latitude(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"latitude": site.latitude}

@router.get("/sites/{site_id}/longitude")
async def get_site_longitude(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"longitude": site.longitude}

@router.get("/sites/{site_id}/name")
async def get_site_name(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"name": site.name}

@router.get("/sites/{site_id}/address")
async def get_site_address(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"address": site.address}

@router.get("/sites/{site_id}/coordinator")
async def get_site_coordinator(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"coordinator": site.coordinator}
