from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MessageSend(BaseModel):
    content: str

@router.post("/chat/groups/{group_id}/messages")
async def send_message(
    group_id: int,
    message: MessageSend,
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
        
    new_msg = models.ChatMessage(
        group_id=group_id,
        sender_id=current_user.id,
        content=message.content
        # files will be added separately or we could add them here via refactoring
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    
    return {
        "id": new_msg.id,
        "group_id": new_msg.group_id,
        "sender_id": new_msg.sender_id,
        "content": new_msg.content,
        "sent_at": new_msg.sent_at
    }
