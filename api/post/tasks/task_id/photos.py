from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from typing import List

router = APIRouter()

@router.post("/tasks/{task_id}/photos")
async def add_task_photos(
    task_id: int, 
    files_list: List[UploadFile] = File(None, alias="files"),
    single_file: UploadFile = File(None, alias="file"),
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Combine inputs into a single list
    files = []
    if files_list:
        files.extend(files_list)
    if single_file:
        files.append(single_file)
    
    if not files:
         raise HTTPException(status_code=422, detail="No files provided. Send fields named 'file' or 'files'.")
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    uploaded_photos = []
    for file in files:
        content = await file.read()
        
        new_photo = models.TaskPhoto(
            task_id=task_id,
            filename=file.filename,
            content=content,
            mime_type=file.content_type
        )
        db.add(new_photo)
        uploaded_photos.append(new_photo)
    
    db.commit()
    
    return [
        {
            "id": p.id,
            "task_id": p.task_id,
            "filename": p.filename,
            "mime_type": p.mime_type,
            "created_at": p.created_at,
            "url": f"/tasks/{task_id}/photos/{p.id}"
        } for p in uploaded_photos
    ]
