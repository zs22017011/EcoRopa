from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from app.schemas.base import UserRole

class UserCreate(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=6)
    role: UserRole

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    credits: float

    class Config:
        orm_mode = True
