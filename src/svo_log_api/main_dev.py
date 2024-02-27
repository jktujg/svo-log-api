from sqlalchemy_utils import create_database, database_exists, drop_database
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from .database import engine
from .models import Base
from .auth.queries import SyncOrm as AuthSyncOrm
from .database import session
from .auth.schemas import UserInDB
from .auth import encryption
from .auth.permissions import UserRole, UserState

from .main import app


class DevSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / 'dev.env')

    ROOT_USER_EMAIL: str
    BASIC_USER_EMAIL: str
    PASSWORD: str


dev_settings = DevSettings()

if database_exists(url=engine.url):
    drop_database(url=engine.url)
create_database(url=engine.url)

engine.echo = False

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

root_user = UserInDB(
    email=dev_settings.ROOT_USER_EMAIL,
    hashed_password=encryption.get_password_hash(dev_settings.PASSWORD),
    role=UserRole.ROOT,
    state=UserState.ACTIVE
)
basic_user = UserInDB(
    email=dev_settings.BASIC_USER_EMAIL,
    hashed_password=encryption.get_password_hash(dev_settings.PASSWORD),
    role=UserRole.USER,
    state=UserState.ACTIVE
)

with session() as conn:
    AuthSyncOrm.create_user(conn, root_user)
    AuthSyncOrm.create_user(conn, basic_user)
