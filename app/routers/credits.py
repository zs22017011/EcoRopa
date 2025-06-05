from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me")
def my_credits(current_user: User = Depends(get_current_user)):
    return {"credits": float(current_user.credits)}

@router.post("/earn/{amount}")
def earn(amount: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.credits += amount
    db.commit()
    return {"credits": float(current_user.credits)}

@router.post("/redeem/{amount}")
def redeem(amount: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.credits < amount:
        return {"error": "Insufficient credits"}
    current_user.credits -= amount
    db.commit()
    return {"credits": float(current_user.credits)}
