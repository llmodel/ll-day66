from sqlmodel import SQLModel, Field
from typing import Optional

class Cafe(SQLModel, table=True):
    """
    Represents a cafe in the database.
    """
    # The primary key for the table, automatically generated.
    id: Optional[int] = Field(default=None, primary_key=True)

    # The name of the cafe. It must be unique and is indexed for faster lookups.
    name: str = Field(unique=True, index=True, max_length=250)

    # URL for the cafe's location on a map.
    map_url: str = Field(max_length=500)

    # URL for an image of the cafe.
    img_url: str = Field(max_length=500)

    # The general location or address of the cafe.
    location: str = Field(max_length=250)

    # Boolean fields indicating amenities.
    has_sockets: bool
    has_toilet: bool
    has_wifi: bool
    can_take_calls: bool

    # Optional fields for cafe details.
    seats: Optional[str] = Field(default=None, max_length=250)
    coffee_price: Optional[str] = Field(default=None, max_length=250)
