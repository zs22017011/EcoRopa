from pydantic import BaseModel

class RecyclePointOut(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
