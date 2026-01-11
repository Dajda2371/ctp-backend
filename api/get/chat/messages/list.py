from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/chat/groups/{group_id}/messages")
async def list_messages(
    group_id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Check membership
    member = db.query(models.ChatMember).filter(
        models.ChatMember.group_id == group_id,
        models.ChatMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this chat")
        
    messages = db.query(models.ChatMessage).filter(models.ChatMessage.group_id == group_id).order_by(models.ChatMessage.sent_at.asc()).all()
    
    result = []
    for msg in messages:
        sender = db.query(models.User).filter(models.User.id == msg.sender_id).first()
        files = db.query(models.ChatFile).filter(models.ChatFile.message_id == msg.id).all()
        
        result.append({
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_name": sender.name if sender else "Unknown",
            "content": msg.content,
            "sent_at": msg.sent_at,
            "files": [
                {
                    "id": f.id,
                    "filename": f.filename,
                    "mime_type": f.mime_type,
                    "url": f"/chat/files/{f.id}"
                } for f in files
            ]
        })
        
    return result
