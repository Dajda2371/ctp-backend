from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from typing import List
import base64
import logging

logger = logging.getLogger("main")

router = APIRouter()

@router.post("/chat/messages/{message_id}/files")
async def add_message_files(
    message_id: int, 
    request: Request,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    msg = db.query(models.ChatMessage).filter(models.ChatMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
        
    # Check sender match? Or just group membership? Ideally sender should upload.
    # But for flexibility let's allow group members (though strictly should be sender)
    if msg.sender_id != current_user.id:
         raise HTTPException(status_code=403, detail="Only sender can attach files to message")

    content_type = request.headers.get("content-type", "")
    uploaded_files = []

    # Handle JSON/Base64
    if "application/json" in content_type:
        try:
            body = await request.json()
            items = body if isinstance(body, list) else [body]
            for item in items:
                filename = item.get("filename", "file")
                b64_content = item.get("content")
                mime_type = item.get("mime_type", "application/octet-stream")
                
                if b64_content:
                    if "," in b64_content:
                        b64_content = b64_content.split(",")[1]
                    file_content = base64.b64decode(b64_content)
                    
                    new_file = models.ChatFile(
                        message_id=message_id,
                        filename=filename,
                        content=file_content,
                        mime_type=mime_type
                    )
                    db.add(new_file)
                    uploaded_files.append(new_file)
        except Exception as e:
            logger.error(f"Chat file upload error: {e}")
            raise HTTPException(status_code=400, detail="Invalid JSON/Base64")

    # Handle Multipart
    else:
        form = await request.form()
        for key, value in form.multi_items():
            if isinstance(value, UploadFile):
                content = await value.read()
                new_file = models.ChatFile(
                    message_id=message_id,
                    filename=value.filename,
                    content=content,
                    mime_type=value.content_type
                )
                db.add(new_file)
                uploaded_files.append(new_file)

    db.commit()
    
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "url": f"/chat/files/{f.id}"
        } for f in uploaded_files
    ]
