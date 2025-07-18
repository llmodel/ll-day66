from fastapi import APIRouter, HTTPException, Depends, Request, Security
from sqlmodel import Session, select, func
from dependencies import get_session
from models.cafe import Cafe
from schemas.cafe import CafeResponse
from middlewares.api_key import get_api_key
import random

router = APIRouter(prefix="/cafe", tags=["cafe"])

#############################################################
@router.get("/random", response_model=CafeResponse)
def get_random_cafe(session: Session = Depends(get_session)):
    """
      Fetches a single random cafe from the database.
    """
    # 1. Get the total count of rows in the Cafe table.
    cafe_count = session.exec(select(func.count(Cafe.id))).one()

    # Add this line for debugging
    print(f"DEBUG: Found {cafe_count} cafes in the database.")
  
    # 2. If the table is empty, raise a 404 error.
    if cafe_count == 0:
        raise HTTPException(status_code=404, detail="No cafes found.")
    
    # 3. Generate a random offset to select a random row.
    random_offset = random.randint(0, cafe_count - 1)

    # 4. Query the database for one cafe at the generated random offset.
    random_cafe = session.exec(select(Cafe).offset(random_offset).limit(1)).first()

    # 5. Return the randomly selected cafe.
    return random_cafe

#############################################################
@router.get("/all", response_model=list[CafeResponse])
def get_all_cafes(session: Session = Depends(get_session)):
    """
        Fetches all cafes from the database.
    """
    return session.exec(select(Cafe)).all()

#############################################################
@router.get("/search", response_model=list[CafeResponse])
def search_cafes(
    request: Request, 
    session: Session = Depends(get_session)
):
    """
        Search for cafes by location. Fetch all cafes from that location.
        user parameter: loc
    """
    # Get the location parameter from the request
    location = request.query_params.get("loc")
    return session.exec(select(Cafe).where(Cafe.location == location)).all()

#############################################################
@router.post("/add", response_model=CafeResponse)
def add_cafe(cafe: Cafe, session: Session = Depends(get_session)):
    """
        Add a new cafe to the database.
    """
    new_cafe = Cafe.model_validate(cafe)
    session.add(new_cafe)
    session.commit()
    session.refresh(new_cafe)
    return new_cafe

#############################################################
@router.patch("/update-price/{cafe_id}", response_model=CafeResponse)
def update_cafe_price(
    cafe_id: int, 
    new_price: str, 
    session: Session = Depends(get_session)
):
    """
        Update the price of a cafe by ID.
    """
    cafe = session.get(Cafe, cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    cafe.coffee_price = new_price
    session.commit()
    session.refresh(cafe)
    return cafe

#############################################################
@router.delete("/report-closed/{cafe_id}", response_model=CafeResponse)
def delete_cafe(
    cafe_id: int, 
    api_key: str = Security(get_api_key),
    session: Session = Depends(get_session)
):
    """
        Delete a cafe by ID.
    """
    cafe = session.get(Cafe, cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    session.delete(cafe)
    session.commit()
    return cafe