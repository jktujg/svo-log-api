from sqlalchemy.orm import Mapped, mapped_column

from tests.fixtures import DatabaseTestCase
from src.svo_log_api.flights_api import field_types
from src.svo_log_api.models import Base


class FieldModel(Base):
    __tablename__ = 'fieldmodels'

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[field_types.created_at]
    updated_at: Mapped[field_types.updated_at]


class TestFieldTypes(DatabaseTestCase):
    def test_created_at(self):
        record = FieldModel()

        self.conn.add(record)
        self.conn.commit()
        self.conn.refresh(record)

        self.assertIsNotNone(record.created_at)

    def test_updated_at(self):
        record = FieldModel()

        self.conn.add(record)
        self.conn.commit()
        self.conn.refresh(record)
        updated_at = record.updated_at
        record.data = 'updated'
        self.conn.commit()

        self.assertNotEqual(record.updated_at, updated_at)
