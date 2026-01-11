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
    result = []
    for task in tasks:
        task_photos = db.query(models.TaskPhoto).filter(models.TaskPhoto.task_id == task.id).all()
        result.append({
            "id": task.id,
            "site_id": task.site_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "assignee": task.assignee,
            "created_at": task.created_at,
            "due_date": task.due_date,
            "latitude": task.latitude,
            "longitude": task.longitude,
            "photos": [
                {
                    "id": p.id,
                    "filename": p.filename,
                    "mime_type": p.mime_type,
                    "url": f"/tasks/{task.id}/photos/{p.id}"
                } for p in task_photos
            ]
        })
    return result
