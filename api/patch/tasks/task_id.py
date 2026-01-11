from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import List, Optional

router = APIRouter()

class TaskUpdate(BaseModel):
    site_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photos: Optional[List[str]] = None

@router.put("/tasks/{task_id}")
@router.patch("/tasks/{task_id}")
async def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    if "site_id" in update_data:
        # Check if new site exists
        site = db.query(models.Site).filter(models.Site.id == update_data["site_id"]).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")
    
    if "priority" in update_data:
        if update_data["priority"] < 1 or update_data["priority"] > 5:
            raise HTTPException(status_code=400, detail="Priority must be between 1 and 5")
            
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    
    return {
        "id": db_task.id,
        "site_id": db_task.site_id,
        "title": db_task.title,
        "description": db_task.description,
        "status": db_task.status,
        "priority": db_task.priority,
        "assignee": db_task.assignee,
        "created_at": db_task.created_at,
        "due_date": db_task.due_date,
        "latitude": db_task.latitude,
        "longitude": db_task.longitude,
        "photos": db_task.photos or []
    }
