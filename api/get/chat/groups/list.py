from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/chat/groups")
async def list_chat_groups(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Get groups where current_user is a member
    memberships = db.query(models.ChatMember).filter(models.ChatMember.user_id == current_user.id).all()
    group_ids = [m.group_id for m in memberships]
    
    groups = db.query(models.ChatGroup).filter(models.ChatGroup.id.in_(group_ids)).all()
    
    result = []
    for g in groups:
        # Get member count or names?
        member_objs = db.query(models.ChatMember).filter(models.ChatMember.group_id == g.id).all()
        # For DM, name might be the other person's name
        display_name = g.name
        if not g.is_group:
            # Find the other member
            other_mem = next((m for m in member_objs if m.user_id != current_user.id), None)
            if other_mem:
                other_user = db.query(models.User).filter(models.User.id == other_mem.user_id).first()
                if other_user:
                    display_name = other_user.name
        
        result.append({
            "id": g.id,
            "name": display_name or "Unnamed Group",
            "is_group": bool(g.is_group),
            "created_at": g.created_at,
            "members_count": len(member_objs)
        })
        
    return result
