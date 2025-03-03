from sqlmodel import SQLModel, Field
from typing import Optional

class ToDo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item: str = Field(index=True, min_length=1, max_length=255)
    status: bool = Field(default=False)
