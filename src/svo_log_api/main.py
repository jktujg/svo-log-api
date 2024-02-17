from fastapi import FastAPI
from sqlalchemy_utils import create_database, database_exists

from .database import engine
from .models import Base
from .flights_api.router import airport_router


if not database_exists(url=engine.url):
    create_database(url=engine.url)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(airport_router, prefix='/api/v1')