from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    donor = "donor"
    business = "business"

class ItemStatus(str, Enum):
    available = "available"
    exchanged = "exchanged"
    donated = "donated"
