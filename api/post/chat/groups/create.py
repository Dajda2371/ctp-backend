from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class GroupCreate(BaseModel):
    name: Optional[str] = None
    user_ids: List[int] # Who to invite
    is_group: bool = True

@router.post("/chat/groups")
async def create_chat_group(
    group: GroupCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # DMs are is_group=False
    if not group.is_group:
        if len(group.user_ids) != 1:
             raise HTTPException(status_code=400, detail="DM must be with exactly one other user")
        
        # Check if DM already exists
        target_id = group.user_ids[0]
        # Logic to check existing DM: intersection of groups for both users where is_group=False
        # Simplified: Just create a new conversation for now, or optimize later.
        
    new_group = models.ChatGroup(
        name=group.name,
        is_group=1 if group.is_group else 0,
        created_at=datetime.utcnow()
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    
    # Add creator
    creator_member = models.ChatMember(
        group_id=new_group.id,
        user_id=current_user.id
    )
    db.add(creator_member)
    
    # Add others
    for uid in group.user_ids:
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == uid).first()
        if user:
            member = models.ChatMember(
                group_id=new_group.id,
                user_id=uid
            )
            db.add(member)
    
    db.commit()
    
    return {
        "id": new_group.id,
        "name": new_group.name,
        "is_group": bool(new_group.is_group),
        "created_at": new_group.created_at
    }
