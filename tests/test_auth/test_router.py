from ..fixtures import AppTestCase
from src.svo_log_api.config import settings
from src.svo_log_api.auth import schemas as auth_schemas
from src.svo_log_api.auth import errors as auth_errors
from src.svo_log_api.auth.encryption import get_password_hash
from src.svo_log_api.auth.queries import SyncOrm


class TestAuthRouter(AppTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.token_url = settings.ROOT_PATH + settings.AUTH_PATH + '/token'

    def setUp(self) -> None:
        super().setUp()
        self.password = 'password'
        self.user_data = auth_schemas.UserInDB(
            email='example@mail.com',
            role=1,
            state=1,
            hashed_password=get_password_hash('password')
        )
        self.user = SyncOrm.create_user(conn=self.conn, new_user=self.user_data)

    def test_login_for_access_token(self):
        response = self.client.post(
            url=self.token_url,
            data=dict(
                username=self.user_data.email,
                password=self.password
            )
        )
        self.assertIn('access_token', response.json())

    def test_login_for_access_token_wrong_password(self):
        response = self.client.post(
            url=self.token_url,
            data=dict(
                username=self.user_data.email,
                password='wrong password'
            )
        )
        self.assertEqual(auth_errors.login_error.detail, response.json().get('detail'))

    def test_login_for_access_token_wrong_email(self):
        response = self.client.post(
            url=self.token_url,
            data=dict(
                username='wrong email',
                password=self.password
            )
        )
        self.assertEqual(auth_errors.login_error.detail, response.json().get('detail'))
