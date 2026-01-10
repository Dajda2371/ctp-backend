from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/sites/{site_id}")
async def get_site(site_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    from sqlalchemy.orm import aliased
    PM = aliased(models.User)
    FM = aliased(models.User)
    
    result = db.query(
        models.Site,
        PM.name.label("pm_name"),
        FM.name.label("fm_name")
    ).outerjoin(PM, models.Site.property_manager == PM.id)\
     .outerjoin(FM, models.Site.facility_manager == FM.id)\
     .filter(models.Site.id == site_id).first()
     
    if not result:
        raise HTTPException(status_code=404, detail="Site not found")
        
    site, pm_name, fm_name = result
    return {
        "id": site.id,
        "name": site.name,
        "address": site.address,
        "latitude": site.latitude,
        "longitude": site.longitude,
        "property_manager": site.property_manager,
        "property_manager_name": pm_name,
        "facility_manager": site.facility_manager,
        "facility_manager_name": fm_name
    }
