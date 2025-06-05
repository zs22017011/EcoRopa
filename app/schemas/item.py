from typing import Optional
from pydantic import BaseModel
from app.schemas.base import ItemStatus

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    size: str
    type: str
    image_url: Optional[str] = None
    latitude: float
    longitude: float

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    size: Optional[str] = None
    type: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[ItemStatus] = None

class ItemOut(ItemBase):
    id: int
    status: ItemStatus
    owner_id: int

    class Config:
        orm_mode = True
