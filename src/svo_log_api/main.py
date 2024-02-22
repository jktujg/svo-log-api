from fastapi import FastAPI

from .flights_api.router import airport_router
from .auth.router import auth_router
from .config import settings


app = FastAPI(root_path=settings.ROOT_PATH)
app.include_router(airport_router, prefix=settings.AIRPORT_PATH)
app.include_router(auth_router, prefix=settings.AUTH_PATH)

