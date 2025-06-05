from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models.recycle_point import RecyclePoint
from app.schemas.recycle_point import RecyclePointOut

router = APIRouter()


