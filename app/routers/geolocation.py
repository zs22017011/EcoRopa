from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models.recycle_point import RecyclePoint
from app.schemas.recycle_point import RecyclePointOut

router = APIRouter()

@router.get("/nearby", response_model=List[RecyclePointOut])
def nearby(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = 5,
    db: Session = Depends(get_db),
):
    
    lat_min = lat - 0.1
    lat_max = lat + 0.1
    lng_min = lng - 0.1
    lng_max = lng + 0.1
    points = db.query(RecyclePoint).filter(
        RecyclePoint.latitude.between(lat_min, lat_max),
        RecyclePoint.longitude.between(lng_min, lng_max)
    ).all()
    return points
