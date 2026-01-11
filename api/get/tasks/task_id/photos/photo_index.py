from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/tasks/{task_id}/photos/{photo_id}")
async def get_task_photo(
    task_id: int, 
    photo_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    photo = db.query(models.TaskPhoto).filter(
        models.TaskPhoto.task_id == task_id,
        models.TaskPhoto.id == photo_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
        
    return Response(content=photo.content, media_type=photo.mime_type)
