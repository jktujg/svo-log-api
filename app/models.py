import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TIMESTAMP


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True)
    }

    def __repr__(self) -> str:
        cols = [f'{col}={getattr(self, col)}' for col in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__}({", ".join(cols)})>'
