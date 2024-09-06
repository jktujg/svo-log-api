import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, drop_database, database_exists

from app.auth.permissions import UserRole, UserState
from app.auth.security import create_access_token
from app.config import settings
from app.database import async_engine
from app.main import app
from app.models import Base
from tests.utils import registered_user


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert async_engine.url.database.startswith('test_'), 'test DB_NAME must ends with `_test`'

    if database_exists(async_engine.url):
        drop_database(async_engine.url)
    create_database(async_engine.url)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    drop_database(async_engine.url)


@pytest.fixture(scope='function', autouse=False)
async def recreate_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await async_engine.dispose()        # to prevent sqlalchemy cache lookup exceptions
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
async def client():
    with TestClient(app=app, root_path=settings.ROOT_PATH) as c:
        yield c


@pytest.fixture(scope='function')
async def session():
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session
        await session.commit()


@pytest.fixture(scope='function')
async def random_user(session):
    email, password, user = await registered_user(session, role=UserRole.USER, state=UserState.ACTIVE)
    return email, password, user


@pytest.fixture(scope='function')
async def random_user_headers(session):
    _, _, user = await registered_user(session, role=UserRole.USER, state=UserState.ACTIVE)
    access_token = create_access_token(user, expires_delta=None)
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture(scope='function')
async def random_superuser_headers(session):
    _, _, user = await registered_user(session, role=UserRole.ROOT, state=UserState.ACTIVE)
    access_token = create_access_token(user, expires_delta=None)
    return {'Authorization': f'Bearer {access_token}'}
