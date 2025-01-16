import logging

from fastapi import FastAPI, Request

from app.core.log_config import setup_logging
from app.routes import text_generation_router, user_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI("Roams Backend IA")

# Include API routes
app.include_router(text_generation_router.router, tags=["text generation"])
app.include_router(user_router.router, tags=["users"])

# Middleware to log requests and responses


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
def health_check():
    return {"status": "OK"}
