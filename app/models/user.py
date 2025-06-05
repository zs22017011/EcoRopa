from sqlalchemy import Column, Integer, String, Enum, DateTime, func, Numeric
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    donor = "donor"
    business = "business"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.donor, nullable=False)
    credits = Column(Numeric(scale=2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
