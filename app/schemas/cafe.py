from pydantic import BaseModel
from typing import Optional


class CafeBase(BaseModel):
  name: str
  map_url: str
  img_url: str
  location: str
  has_sockets: bool
  has_toilet: bool
  has_wifi: bool
  can_take_calls: bool
  seats: Optional[str]
  coffee_price: Optional[str]

  class Config:
    orm_mode = True


class CafeCreate(CafeBase):
  pass

class CafeResponse(CafeBase):
  id: int
  