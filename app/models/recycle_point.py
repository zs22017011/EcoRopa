from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base


class RecyclePoint(Base):
    __tablename__ = "recycle_points"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    address = Column(String(256))
    latitude = Column(Float)
    longitude = Column(Float)