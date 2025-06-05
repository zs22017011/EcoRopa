from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.models.item import Item, ItemStatus
from app.models.user import User
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = Item(owner_id=current_user.id, **item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/", response_model=List[ItemOut])
def list_items(
    db: Session = Depends(get_db),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(10),
    type: Optional[str] = Query(None),
    size: Optional[str] = Query(None)
):
    query = db.query(Item).filter(Item.status == ItemStatus.available)

    if type:
        query = query.filter(Item.type.ilike(f"%{type}%"))
    if size:
        query = query.filter(Item.size == size)

    if latitude is not None and longitude is not None:
        lat_min = latitude - 0.1
        lat_max = latitude + 0.1
        lon_min = longitude - 0.1
        lon_max = longitude + 0.1
        query = query.filter(
            Item.latitude.between(lat_min, lat_max),
            Item.longitude.between(lon_min, lon_max)
        )

    return query.all()

@router.get("/{item_id}", response_model=ItemOut)
def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemOut)
def update_item(
    item_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    db.delete(item)
    db.commit()
