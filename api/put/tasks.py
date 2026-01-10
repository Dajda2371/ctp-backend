from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from auth_utils import get_current_user
from datetime import datetime
from typing import Optional

router = APIRouter()

class SiteIdUpdate(BaseModel):
    site_id: int

class TitleUpdate(BaseModel):
    title: str

class DescriptionUpdate(BaseModel):
    description: Optional[str] = None

class StatusUpdate(BaseModel):
    status: str

class PriorityUpdate(BaseModel):
    priority: int

class AssigneeUpdate(BaseModel):
    assignee: Optional[str] = None

class DueDateUpdate(BaseModel):
    due_date: Optional[datetime] = None

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

@router.put("/tasks/{task_id}/title")
async def update_task_title(task_id: int, title_update: TitleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = title_update.title
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}/description")
async def update_task_description(task_id: int, desc_update: DescriptionUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.description = desc_update.description
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}/status")
async def update_task_status(task_id: int, status_update: StatusUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.status = status_update.status
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}/priority")
async def update_task_priority(task_id: int, priority_update: PriorityUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if priority_update.priority < 1 or priority_update.priority > 5:
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 5")
        
    db_task.priority = priority_update.priority
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}/assignee")
async def update_task_assignee(task_id: int, assignee_update: AssigneeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.assignee = assignee_update.assignee
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}/due_date")
async def update_task_due_date(task_id: int, date_update: DueDateUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.due_date = date_update.due_date
    db.commit()
    db.refresh(db_task)
    return db_task
