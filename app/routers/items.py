from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.models.item import Item, ItemStatus
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ItemOut, status_code=201)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = Item(owner_id=current_user.id, **item_in.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemOut])
def list_items(
    db: Session = Depends(get_db),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(10),
    type: Optional[str] = None,
    size: Optional[str] = None
):
    query = db.query(Item).filter(Item.status == ItemStatus.available)
    if type:
        query = query.filter(Item.type.ilike(f"%{type}%"))
    if size:
        query = query.filter(Item.size == size)
    if latitude and longitude:
        lat_min = latitude - 0.1
        lat_max = latitude + 0.1
        lon_min = longitude - 0.1
        lon_max = longitude + 0.1
        query = query.filter(Item.latitude.between(lat_min, lat_max)).filter(Item.longitude.between(lon_min, lon_max))
    return query.all()

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(item)
    db.commit()
