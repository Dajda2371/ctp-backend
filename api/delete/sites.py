from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.delete("/sites/{site_id}")
async def delete_site(
    site_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Check if there are associated tasks
    tasks_count = db.query(models.Task).filter(models.Task.site_id == site_id).count()
    if tasks_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete site with associated tasks. Delete tasks first.")
    
    db.delete(db_site)
    db.commit()
    
    return {"message": "Site deleted successfully"}
