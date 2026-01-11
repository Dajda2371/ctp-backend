from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from typing import List

router = APIRouter()

import logging

logger = logging.getLogger("main")

import base64
from pydantic import BaseModel
from typing import Optional

class PhotoBase64(BaseModel):
    filename: str
    content: str # Base64 encoded string
    mime_type: str = "image/jpeg"

@router.post("/tasks/{task_id}/photos")
async def add_task_photos(
    task_id: int, 
    request: Request,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    logger.info(f"Received photo upload request for task {task_id}")
    content_type = request.headers.get("content-type", "")
    
    uploaded_photos = [] # Define here to be accessible in both branches
    
    # Handle JSON (Base64) Uploads - Best for React Native
    if "application/json" in content_type:
        logger.info("Processing JSON Base64 upload")
        try:
            body = await request.json()
            # Support both single object and list of objects
            items = body if isinstance(body, list) else [body]
            
            for item in items:
                # Validate simple dict against our logic
                filename = item.get("filename", "upload.jpg")
                b64_content = item.get("content")
                mime_type = item.get("mime_type", "image/jpeg")
                
                if not b64_content:
                    continue
                    
                # Decode Base64
                try:
                    if "," in b64_content:
                        b64_content = b64_content.split(",")[1]
                    file_content = base64.b64decode(b64_content)
                except Exception as e:
                    logger.error(f"Failed to decode base64: {e}")
                    continue

                new_photo = models.TaskPhoto(
                    task_id=task_id,
                    filename=filename,
                    content=file_content,
                    mime_type=mime_type
                )
                db.add(new_photo)
                uploaded_photos.append(new_photo)
                
        except Exception as e:
            logger.error(f"JSON processing failed: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON body: {str(e)}")

    # Handle Multipart Uploads - Best for Web
    else: 
        logger.info("Processing Multipart upload")
        form = await request.form()
        files = []
        
        # Iterate over all form fields to find files
        for key, value in form.multi_items():
            if isinstance(value, UploadFile):
                files.append(value)
                logger.info(f"Found file in field '{key}': {value.filename}")

        if not files:
             logger.error("No files found in request")
             logger.info(f"Form keys received: {list(form.keys())}")
             raise HTTPException(status_code=422, detail="No files provided. Send form-data or JSON with Base64.")

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
    
    # Common Commit Logic
    if not uploaded_photos:
         raise HTTPException(status_code=422, detail="No valid photos processed.")

    logger.info(f"Committing {len(uploaded_photos)} photos to database...")
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
