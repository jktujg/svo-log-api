from ..fixtures import AppTestCase
from src.svo_log_api.auth import schemas as auth_schemas
from src.svo_log_api.auth import models as auth_models


class TestAuthModels(AppTestCase):
    def test_user_model(self):
        user = auth_schemas.UserInDB(email='example@mail.com', role=0, state=0, hashed_password='hashed_password')
        user_model = auth_models.UserModel(**user.model_dump())

        self.conn.add(user_model)
        self.conn.commit()
        self.assertIsNotNone(user_model.id)
