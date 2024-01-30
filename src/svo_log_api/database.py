from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config.config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        cols = [f'{col}={getattr(self, col)}' for col in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__}({", ".join(cols)})>'
