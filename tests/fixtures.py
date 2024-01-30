from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from unittest import TestCase

from src.svo_log_api.config.config import settings
from src.svo_log_api import models


class DatabaseTestCase(TestCase):
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

    @classmethod
    def tearDownClass(cls) -> None:
        if database_exists(cls.engine.url):
            drop_database(cls.engine.url)

    def setUp(self) -> None:
        models.Base.metadata.create_all(bind=self.engine)
        self.conn = sessionmaker(bind=self.engine)()

    def tearDown(self) -> None:
        self.conn.close()
        models.Base.metadata.drop_all(bind=self.engine)
