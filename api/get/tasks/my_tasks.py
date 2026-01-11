from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/tasks/me")
async def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Filter tasks where the assignee matches the current user's name or email
    query = db.query(models.Task).filter(
        or_(
            models.Task.assignee == current_user.name,
            models.Task.assignee == current_user.email
        )
    )
    
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
