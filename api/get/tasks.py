from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from typing import Optional

router = APIRouter()

@router.get("/tasks")
async def get_tasks(
    site_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Task)
    if site_id:
        query = query.filter(models.Task.site_id == site_id)
    if status:
        query = query.filter(models.Task.status == status)
    
    tasks = query.all()
    return [
        {
            "id": str(task.id),
            "site_id": str(task.site_id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "assignee": task.assignee,
            "created_at": task.created_at,
            "due_date": task.due_date,
            "photos": task.photos
        } for task in tasks
    ]

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": str(task.id),
        "site_id": str(task.site_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "assignee": task.assignee,
        "created_at": task.created_at,
        "due_date": task.due_date,
        "photos": task.photos
    }
