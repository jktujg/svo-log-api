import uvicorn
from fastapi import FastAPI
from .flights_api.router import airport_router
from .auth.router import auth_router
from .config import settings
from .logger import log_config

app = FastAPI(root_path=settings.ROOT_PATH)
app.include_router(airport_router, prefix=settings.AIRPORT_PATH)
app.include_router(auth_router, prefix=settings.AUTH_PATH)


if __name__ == '__main__':
    uvicorn.run('src.svo_log_api.main:app', port=8092, log_config=log_config)
