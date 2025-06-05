from .user import User
from .item import Item
from .recycle_point import RecyclePoint
from .message import Message
from sqlalchemy.orm import relationship
User.items = relationship("Item", back_populates="owner")
