from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user

router = APIRouter()

class SiteIdUpdate(BaseModel):
    site_id: int

@router.put("/tasks/{task_id}/site_id")
async def update_task_site_id(task_id: int, site_update: SiteIdUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    site = db.query(models.Site).filter(models.Site.id == site_update.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
        
    db_task.site_id = site_update.site_id
    db.commit()
    db.refresh(db_task)
    return db_task
