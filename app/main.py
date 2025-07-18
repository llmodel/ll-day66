# src/main.py

##### To start the FastAPI app
#####     uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload
#####     with uv: uv run fastapi dev

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from middlewares.logger import StatusCodeLoggerMiddleware,configure_fastapi_logging, setup_logger
from core.config import settings
from dependencies import init_db
from routers import root, cafe
from fastapi.staticfiles import StaticFiles  # <-- Import this


#####  STARTUP / SHUTDOWN EVENTS  #####
@asynccontextmanager
async def lifespan(app: FastAPI):
    ##### STARTUP ACTIONS #####
    logger.info('asynccontexmanager - app startup')
    init_db()
    yield

    ##### SHUTDOWN ACTIONS #####
    logger.info("Application shutdown")

#####  MAIN SECTION  #####
app = FastAPI(lifespan=lifespan)

# Setup shared logger
logger = setup_logger(
    name=settings.LOG_NAME,
    log_file=settings.LOG_FILE,
    log_level=logging.INFO
)

# Configure FastAPI and Uvicorn logging in the logging middleware
configure_fastapi_logging(logger=logger)

# Add middleware for request/response logging
app.add_middleware(
    StatusCodeLoggerMiddleware, 
    logger=logger
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
# This makes the 'static' folder available under the URL path "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(root.router)
app.include_router(cafe.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
