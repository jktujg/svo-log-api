from fastapi import FastAPI
from sqlalchemy_utils import create_database, database_exists

from .database import engine, Base
from . import models
from .routers.airport_router import airport_router


if not database_exists(url=engine.url):
    create_database(url=engine.url)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(airport_router, prefix='/api/v1')