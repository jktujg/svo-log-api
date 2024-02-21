from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from unittest import TestCase
from fastapi.testclient import TestClient

from src.svo_log_api.config import settings
from src.svo_log_api import models
from src.svo_log_api.main import app
from src.svo_log_api.dependencies import get_session


class AppTestCase(TestCase):
    engine: Engine

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine(
            url=settings.TEST_DATABASE_URL_psycopg,
            echo=False,
        )

        if database_exists(cls.engine.url):
            drop_database(cls.engine.url)
        create_database(cls.engine.url)

        cls.session = sessionmaker(bind=cls.engine)

        def get_test_session(**params):
            def session_gen():
                with cls.session(**params) as conn:
                    yield conn
            return session_gen

        app.dependency_overrides[get_session] = get_test_session
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        if database_exists(cls.engine.url):
            drop_database(cls.engine.url)

    def setUp(self) -> None:
        models.Base.metadata.create_all(bind=self.engine)
        self.conn = self.session()

    def tearDown(self) -> None:
        self.conn.close()
        models.Base.metadata.drop_all(bind=self.engine)
