from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from .config import settings
from .routes import api_router
from .middleware import log_requests


app = FastAPI(
    root_path=settings.ROOT_PATH,
    title='SvologAPI',
    version='0.1.0',
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.middleware('http')(log_requests)

app.include_router(api_router)
