from pydantic import BaseModel
from datetime import datetime
from typing import List

class Zone(BaseModel):
    zone_id: str
    capacity: str
    price: str
    name: str
    numbered: str

class Event(BaseModel):
    id: int
    name: str
    starts_at: datetime
    ends_at: datetime
    zones: List[Zone]
