from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Float, func
import enum
from sqlalchemy.orm import relationship
from app.db.session import Base

class ItemStatus(str, enum.Enum):
    available = "available"
    exchanged = "exchanged"
    donated = "donated"

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(130))
    description = Column(String(512))
    size = Column(String(16))
    type = Column(String(64))
    image_url = Column(String(258))
    status = Column(Enum(ItemStatus), default=ItemStatus.available)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="items")
