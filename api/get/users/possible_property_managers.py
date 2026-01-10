from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
import models
from auth_utils import get_current_user

router = APIRouter()

@router.get("/users/possible_property_manager")
async def get_possible_property_managers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    users = db.query(models.User).filter(
        or_(
            models.User.role == "property_manager",
            models.User.role == "admin"
        )
    ).all()
    return [
        {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role
        } for user in users
    ]
