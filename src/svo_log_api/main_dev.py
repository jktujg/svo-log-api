import uvicorn

from .database import engine
from .logger import log_config
from .main import app
from .flights_api.dependencies import upsert_permission


app.dependency_overrides[upsert_permission] = lambda: True


engine.echo = False


if __name__ == '__main__':
    uvicorn.run('src.svo_log_api.main:app', reload=True, port=8098, log_config=log_config)
