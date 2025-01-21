import logging.config
import time
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.dependencies import get_settings
from app.error.exceptions import CustomException
from app.routes import model_router, text_generation_router, user_router
from app.core.log_config import LogConfig

logging.config.dictConfig(LogConfig().model_dump())

logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title="Roams AI API",
    description="""
    AI-powered text generation API with customizable model parameters.
    
    ## Features
    * Text generation using AI models
    * Model parameter customization
    * User authentication
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Model",
            "description": "Operations with AI model configuration",
        },
        {
            "name": "Text generation",
            "description": "Generate text using AI models",
        },
        {
            "name": "Users",
            "description": "User management and authentication",
        },
    ]
)

# Include API routes
app.include_router(model_router.router, tags=["Model"])
app.include_router(text_generation_router.router, tags=["Text generation"])
app.include_router(user_router.router, tags=["Users"])


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.error}
    )


# Middleware to log requests and responses
@app.middleware("http")
async def log_request_response(request: Request, call_next):
    request_id = str(uuid4())
    start_time = time.time()

    # Log request metadata
    path = request.url.path + \
        ("?" + request.url.query if request.url.query else "")
    logger.info(f"Request {request_id}: {request.method} {path}")

    # Process request
    response = await call_next(request)

    # Log response metadata
    process_time = round((time.time() - start_time) * 1000)
    logger.info(
        f"Response {request_id}: Status={
            response.status_code} Duration={process_time}ms "
        f"Method={request.method} Path={path}"
    )

    return response


@app.get("/")
def health_check():
    return {"status": "OK"}
