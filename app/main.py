import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.error.exceptions import AuthenticationException, CustomException
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
async def logging_middleware(request: Request, call_next):
    try:
        # Log request
        request_logger.info(f"Request: {request.method} {request.url}")
        request_logger.info(f"Headers: {dict(request.headers)}")

        # Process request
        response = await call_next(request)

        # Get response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # Create new response with consumed body
        new_response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )

        # Log response with details
        request_logger.info(f"Response: {response.status_code}")
        request_logger.info(f"Headers: {dict(response.headers)}")

        try:
            body = json.loads(response_body)
            request_logger.info(f"Body: {body}")
        except:
            request_logger.info(f"Body: {response_body.decode()}")

        return new_response

    except Exception as e:
        # Log error
        request_logger.error(f"Error processing {request.method} {
                             request.url}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )


@app.get("/")
def health_check():
    return {"status": "OK"}
