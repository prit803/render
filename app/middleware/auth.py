from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
from app.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith('/secure'):
            token = request.headers.get('Authorization')
            if not token:
                raise HTTPException(status_code=401, detail='Missing token')
            try:
                payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            except Exception:
                raise HTTPException(status_code=401, detail='Invalid token')
        response = await call_next(request)
        return response
