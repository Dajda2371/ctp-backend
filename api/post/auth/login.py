from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import auth_utils
from .schemas import UserAuth

router = APIRouter()

@router.post("/login")
async def login(user: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth_utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    return {
        "access_token": "authenticated_access_token", 
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "role": db_user.role
        }
    }

@router.get("/me")
async def get_me(db: Session = Depends(get_db)):
    # For now, since we don't have JWT, we'll return the first user as a dummy 'me'
    # or a 401 if no users exist. In production, this would use a token.
    user = db.query(models.User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    }
