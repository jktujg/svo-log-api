from typing import Optional, Sequence

from sqlalchemy import ForeignKey, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class AircraftModel(Base):
    __tablename__ = 'aircrafts'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[Optional[int]] = mapped_column(unique=True, nullable=True)
    name: Mapped[Optional[str]]


class CountryModel(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    region: Mapped[str]

    airports = relationship('AirportModel', back_populates='country')


class AirportModel(Base):
    __tablename__ = 'airports'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[int] = mapped_column(unique=True)
    iata: Mapped[str] = mapped_column(String(3), unique=True)
    icao: Mapped[str] = mapped_column(String(4), unique=True)
    code_ru: Mapped[Optional[str]] = mapped_column(String(3))
    name: Mapped[str]
    name_ru: Mapped[str]
    city_ru: Mapped[str]
    city_en: Mapped[str]
    lat: Mapped[Optional[float]] = mapped_column(DECIMAL(9, 6))
    long: Mapped[Optional[float]] = mapped_column(DECIMAL(9, 6))
    timezone: Mapped[Optional[str]]
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id', ondelete='set null'))

    country = relationship('CountryModel', back_populates='airports', lazy='joined')


