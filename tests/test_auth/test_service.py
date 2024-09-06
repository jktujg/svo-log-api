import pytest
from fastapi import HTTPException

from app.auth.service import register_user


@pytest.mark.usefixtures('recreate_tables',)
class TestService:
    async def test_register_user(self,session):
        user = await register_user(session, email='some@mail.com', password='Strong123', role=1, state=2)

        assert user.email == 'some@mail.com'

        with pytest.raises(HTTPException) as err:
            assert await register_user(session, email='some@mail.com', password='Strong123', role=1, state=2), 'duplicate user'
        await session.rollback()

    async def test_register_user_weak_password(self, session):
        with pytest.raises(HTTPException):
            await register_user(session, email='some@mail.com', password='weak', role=1, state=2)

    async def test_register_user_invalid_data(self,session):
        with pytest.raises(HTTPException):
            await register_user(session, email='invalid_email', password='Strong123', role=1, state=2)
