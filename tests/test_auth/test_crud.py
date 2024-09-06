import pytest
from sqlalchemy.exc import IntegrityError

from app.auth.crud import AsyncOrm
from app.auth.schemas import UserInDB


@pytest.mark.usefixtures('recreate_tables',)
class TestCrud:
    async def test_create_user(self, session):
        new_user = UserInDB(email='some@mail.com', role=1, state=2, hashed_password='password_hash')
        created_user = await AsyncOrm.create_user(session, new_user)

        assert created_user.id
        assert created_user.email == 'some@mail.com'
        assert created_user.hashed_password == 'password_hash'
        assert created_user.role == 1
        assert created_user.state == 2

    async def test_create_user_duplicate_email(self, session):
        new_user = UserInDB(email='some@mail.com', role=1, state=2, hashed_password='password_hash')
        await AsyncOrm.create_user(session, new_user)

        with pytest.raises(IntegrityError):
            await AsyncOrm.create_user(session, new_user)
        await session.rollback()

    async def test_get_user_exists(self, session, random_user):
        username, password, user = random_user
        user_indb = await AsyncOrm.get_user(session, email=username)

        assert user_indb.id
        assert user_indb.email == username
        assert user_indb.hashed_password == user.hashed_password

    async def test_get_user_not_exists(self, session):
        user = await AsyncOrm.get_user(session, email='notexists@mail.com')

        assert user is None
