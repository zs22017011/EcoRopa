from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/credits", tags=["Credits"])

@router.get("/me", response_model=dict)
def get_credits(current_user: User = Depends(get_current_user)):
    return {"credits": float(current_user.credits)}

@router.post("/earn/{amount}", response_model=dict)
def earn_credits(
    amount: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.credits += amount
    db.commit()
    db.refresh(current_user)
    return {"credits": float(current_user.credits)}

@router.post("/redeem/{amount}", response_model=dict)
def redeem_credits(
    amount: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.credits < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient credits"
        )
    current_user.credits -= amount
    db.commit()
    db.refresh(current_user)
    return {"credits": float(current_user.credits)}
