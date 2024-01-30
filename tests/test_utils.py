from unittest import TestCase
from src.svo_log_api import utils
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TestModel(Base):
    __tablename__ = 'test_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    full_name: Mapped[str]
    value: Mapped[float]


class TestUtils(TestCase):
    def test_unique_schemas(self):
        class TestModel(BaseModel):
            i: int
            s: str
        t1 = TestModel(i=1, s='a')
        t2 = TestModel(i=2, s='a')
        t3 = TestModel(i=1, s='b')
        t4 = TestModel(i=2, s='b')

        unique_models = utils.unique_schemas([t1, t2, t3, t4], unique_keys=['i', 's'])
        self.assertListEqual(unique_models, [t1, t4])

    def test_get_columns_all(self):
        columns = utils.get_columns(model=TestModel, include_primary=True)
        self.assertListEqual(list(columns), list(TestModel.__table__.columns.keys()))

    def test_get_columns_exclude(self):
        columns = utils.get_columns(model=TestModel, exclude=['value', 'full_name'], include_primary=True)
        self.assertListEqual(list(columns), ['id', 'name'])

    def test_get_columns_exclude_primary(self):
        columns = utils.get_columns(model=TestModel, exclude=[])
        self.assertListEqual(list(columns), ['name', 'full_name', 'value'])
