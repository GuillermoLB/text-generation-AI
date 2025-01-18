import logging
from fastapi import FastAPI, Request
from app.routes import model_router, text_generation_router, user_router
from app.core.log_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)
request_logger = logging.getLogger("request_logger")

app = FastAPI(title="Roams Backend IA")

# Include API routes
app.include_router(model_router.router, tags=["Model"])
app.include_router(text_generation_router.router, tags=["Text generation"])
app.include_router(user_router.router, tags=["Users"])

# Middleware to log requests and responses


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    request_logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
def health_check():
    return {"status": "OK"}
