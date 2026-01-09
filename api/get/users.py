from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/users")
async def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    users = db.query(models.User).all()
    return [
        {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role
        } for user in users
    ]
