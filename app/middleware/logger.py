import logging
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

def setup_logging(app: FastAPI):
    logger = logging.getLogger("uvicorn.access")
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response: Response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
