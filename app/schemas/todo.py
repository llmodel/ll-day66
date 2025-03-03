from pydantic import BaseModel
from typing import Optional

class ToDoBase(BaseModel):
    item: str
    status: Optional[bool] = False

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(BaseModel):
    item: Optional[str] = None
    status: Optional[bool] = None

class ToDoResponse(ToDoBase):
    id: int

    class Config:
        from_attributes = True
