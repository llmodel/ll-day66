# app/routers/root.py
from fastapi import APIRouter, Depends, Security, Request
from dependencies import get_logger
from middlewares.api_key import get_api_key
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def root(
  request: Request,
  # api_key: str = Security(get_api_key),
  logger=Depends(get_logger)
):
  logger.info("Root endpoint accessed")
  # return {"message": "Welcome to the FastAPI starter app!"}
  dynamic_data = {"request": request, "title": "Welcome to the Cafes API (v0.1)"}
  # return templates.TemplateResponse("index.html", {"request": request})
  return templates.TemplateResponse("index.html", dynamic_data)
