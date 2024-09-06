from fastapi import APIRouter

from .config import settings
from .auth.router import auth_router
from .flights_api.router import airport_router


api_router = APIRouter()

api_router.include_router(airport_router, prefix=settings.AIRPORT_PATH)
api_router.include_router(auth_router, prefix=settings.AUTH_PATH)
