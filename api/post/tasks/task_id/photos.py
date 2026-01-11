from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.post("/tasks/{task_id}/photos")
async def add_task_photo(
    task_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    content = await file.read()
    
    new_photo = models.TaskPhoto(
        task_id=task_id,
        filename=file.filename,
        content=content,
        mime_type=file.content_type
    )
    db.add(new_photo)
    
    # Optional: Keep the metadata JSON in sync if needed, e.g., storing the photo ID
    # current_photos = list(db_task.photos) if db_task.photos else []
    # current_photos.append(str(new_photo.id))
    # db_task.photos = current_photos
    
    db.commit()
    db.refresh(new_photo)
    
    return {
        "id": new_photo.id,
        "task_id": new_photo.task_id,
        "filename": new_photo.filename,
        "mime_type": new_photo.mime_type,
        "created_at": new_photo.created_at
    }
