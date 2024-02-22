from sqlalchemy.exc import IntegrityError

from ..fixtures import AppTestCase
from src.svo_log_api.auth.queries import SyncOrm
from src.svo_log_api.auth import schemas as auth_schemas
from src.svo_log_api.auth import models as auth_models


class TestAuthQueries(AppTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_data = auth_schemas.UserInDB(email='example@mail.com', role=0, state=0, hashed_password='hashed_password')

    def test_get_user(self):
        user_model = auth_models.UserModel(**self.user_data.model_dump())
        self.conn.add(user_model)
        self.conn.commit()

        found_user = SyncOrm.get_user(conn=self.conn, email=self.user_data.email)
        self.assertIs(found_user, user_model)

    def test_get_user_not_found_return_none(self):
        found_user = SyncOrm.get_user(conn=self.conn, email='not in database')
        self.assertIsNone(found_user)

    def test_create_user(self):
        created_user = SyncOrm.create_user(conn=self.conn, new_user=self.user_data)
        self.assertEqual(created_user.email, self.user_data.email)

    def test_create_user_same_email_raises(self):
        SyncOrm.create_user(conn=self.conn, new_user=self.user_data)
        with self.assertRaises(IntegrityError):
            SyncOrm.create_user(conn=self.conn, new_user=self.user_data)


