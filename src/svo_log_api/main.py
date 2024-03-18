import uvicorn
from fastapi import FastAPI
from .flights_api.router import airport_router
from .auth.router import auth_router
from .config import settings
from .logger import log_config
from .database import engine
from sqlalchemy_utils import create_database, database_exists
from .auth import models as auth_models
from .flights_api import models as flight_models
from .models import Base


if not database_exists(url=engine.url):
    create_database(url=engine.url)

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path=settings.ROOT_PATH)
app.include_router(airport_router, prefix=settings.AIRPORT_PATH)
app.include_router(auth_router, prefix=settings.AUTH_PATH)


if __name__ == '__main__':
    uvicorn.run('src.svo_log_api.main:app', port=8092, log_config=log_config)
