from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from typing import List

router = APIRouter()

import logging

logger = logging.getLogger("main")

@router.post("/tasks/{task_id}/photos")
async def add_task_photos(
    task_id: int, 
    request: Request,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    logger.info(f"Received photo upload request for task {task_id}")
    
    form = await request.form()
    files = []
    
    # Iterate over all form fields to find files
    for key, value in form.multi_items():
        if isinstance(value, UploadFile):
            files.append(value)
            logger.info(f"Found file in field '{key}': {value.filename}")

    logger.info(f"Number of files processed: {len(files)}")

    if not files:
         logger.error("No files found in request")
         # Log available keys to help debugging
         logger.info(f"Form keys received: {list(form.keys())}")
         raise HTTPException(status_code=422, detail="No files provided. Send form-data with any file field.")

    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        logger.error(f"Task {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    
    uploaded_photos = []
    for file in files:
        logger.info(f"Processing file: {file.filename}, content_type: {file.content_type}")
        content = await file.read()
        logger.info(f"Read {len(content)} bytes")
        
        new_photo = models.TaskPhoto(
            task_id=task_id,
            filename=file.filename,
            content=content,
            mime_type=file.content_type
        )
        db.add(new_photo)
        uploaded_photos.append(new_photo)
    
    logger.info("Committing to database...")
    db.commit()
    logger.info("Commit successful")
    
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
