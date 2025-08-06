from fastapi import FastAPI
from app.api.routes import router
from app.middleware.logger import setup_logging
from app.middleware.auth import AuthMiddleware

app = FastAPI()
setup_logging(app)
app.include_router(router)
