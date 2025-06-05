from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserUpdate
from app.deps import get_db, get_current_user
from app.models.user import User
from app.core.security import hash_password

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_me(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.name is not None:
        current_user.name = data.name
    if data.email is not None:
        current_user.email = data.email
    if data.password is not None:
        current_user.hashed_password = hash_password(data.password)
    if data.role is not None:
        current_user.role = data.role
    db.commit()
    db.refresh(current_user)
    return current_user
