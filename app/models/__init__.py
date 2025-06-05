from .user import User

User.items = relationship("Item", back_populates="owner")
