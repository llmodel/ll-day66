# app/depedencies.py

import logging
from core.config import settings
from sqlmodel import SQLModel, create_engine, Session

db_path = settings.DATABASE_PATH
engine = create_engine(f"sqlite:///{db_path}", echo=True)

def get_logger():
  # find and return a logger by name - for dependency injection
  return logging.getLogger(settings.LOG_NAME)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
  with Session(engine) as session:
    yield session