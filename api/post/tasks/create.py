from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from typing import List, Optional

router = APIRouter()

class TaskCreate(BaseModel):
    site_id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = "TODO"
    priority: Optional[int] = 3
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photos: Optional[List[str]] = None

@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Check if site exists
    site = db.query(models.Site).filter(models.Site.id == task.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
        
    if task.priority and (task.priority < 1 or task.priority > 5):
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 5")
        
    new_task = models.Task(
        site_id=task.site_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assignee=task.assignee,
        due_date=task.due_date,
        latitude=task.latitude,
        longitude=task.longitude,
        photos=task.photos
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {
        "id": str(new_task.id),
        "site_id": str(new_task.site_id),
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "priority": new_task.priority,
        "assignee": new_task.assignee,
        "created_at": new_task.created_at,
        "due_date": new_task.due_date,
        "latitude": new_task.latitude,
        "longitude": new_task.longitude,
        "photos": new_task.photos
    }
