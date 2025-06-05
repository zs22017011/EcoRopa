from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageOut
from app.models.user import User

router = APIRouter()

@router.post("/{receiver_id}", response_model=MessageOut, status_code=201)
def send_message(receiver_id: int, data: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message = Message(sender_id=current_user.id, receiver_id=receiver_id, content=data.content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("/", response_model=List[MessageOut])
def inbox(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Message).filter(Message.receiver_id == current_user.id).order_by(Message.sent_at.desc()).all()
