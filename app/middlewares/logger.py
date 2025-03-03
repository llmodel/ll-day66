# src/middlewares/logger.py

import logging
import logging.handlers
# import sys
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

def setup_logger(name: str, log_file: str = 'app.log', log_level=logging.INFO):
    # Create a single logger instance
    logger = logging.getLogger(name)
    logger.setLevel(log_level)  # Set the minimum logging level

    # Check if a logger already has handlers
    if not logger.handlers:
        # Create a handler for the log file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # Create a formatter and set it on the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False

    return logger

class StatusCodeLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: logging.Logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        self.logger.info(f"Request: {request.method} {request.url.path} - Status: {response.status_code}")
        return response
    
def configure_fastapi_logging(logger: logging.Logger):
    # Configure FastAPI and Uvicorn and other loggers
    loggers_to_configure = [
        'uvicorn',
        'uvicorn.error',
        'uvicorn.access',
        'fastapi'
        'sqlmodel'
    ]
    # Use the first handler from the shared logger
    shared_handler = logger.handlers[0] if logger.handlers else None
    if shared_handler is None:
        raise RuntimeError("The shared logger must have at least one handler.")
    
    for logger_name in loggers_to_configure:
        log = logging.getLogger(logger_name)
        log.handlers = []  # Remove any existing handlers
        log.addHandler(shared_handler) # Use the shared handler
        log.setLevel(logger.level)
        log.propagate = False
    
# Add a shared logger instance
# logger = setup_logger("FASTAPI", "fast_api.log")