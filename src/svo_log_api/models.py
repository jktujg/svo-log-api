from datetime import datetime
from typing import Optional, Sequence, Literal
from enum import Enum

from sqlalchemy import ForeignKey, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .field_types import created_at, updated_at


class AircraftModel(Base):
    __tablename__ = 'aircrafts'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[Optional[int]] = mapped_column(unique=True, nullable=True)
    name: Mapped[Optional[str]]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class CountryModel(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    region: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

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

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    country = relationship('CountryModel', back_populates='airports', lazy='joined')


class CompanyModel(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    iata: Mapped[str] = mapped_column(String(2), unique=True)
    name: Mapped[Optional[str]]
    url_buy: Mapped[Optional[str]]
    url_register: Mapped[Optional[str]]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Direction(Enum):
    arrival = 'arrival'
    departure = 'departure'


class FlightModel(Base):
    __tablename__ = 'flights'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[int] = mapped_column(unique=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id', ondelete='set null'))

    mar1_id: Mapped[int] = mapped_column(ForeignKey('airports.id', ondelete='set null'), nullable=True)
    mar2_id: Mapped[int] = mapped_column(ForeignKey('airports.id', ondelete='set null'), nullable=True)
    mar3_id: Mapped[int] = mapped_column(ForeignKey('airports.id', ondelete='set null'), nullable=True)
    mar4_id: Mapped[int] = mapped_column(ForeignKey('airports.id', ondelete='set null'), nullable=True)
    mar5_id: Mapped[int] = mapped_column(ForeignKey('airports.id', ondelete='set null'), nullable=True)
    aircraft_id: Mapped[int] = mapped_column(ForeignKey('aircrafts.id', ondelete='set null'), nullable=True)

    direction: Mapped[Direction]
    number: Mapped[int]
    date: Mapped[datetime]
    main_id: Mapped[Optional[int]]
    way_time: Mapped[Optional[int]]
    # check-in
    chin_start: Mapped[Optional[datetime]]
    chin_end: Mapped[Optional[datetime]]
    chin_start_et: Mapped[Optional[datetime]]
    chin_end_et: Mapped[Optional[datetime]]
    chin_id: Mapped[Optional[str]]
    # boarding
    boarding_start: Mapped[Optional[datetime]]
    boarding_end: Mapped[Optional[datetime]]
    gate_id: Mapped[Optional[str]]
    gate_id_prev: Mapped[Optional[str]]
    # terminal
    term_local: Mapped[Optional[str]]
    term_local_prev: Mapped[Optional[str]]
    # bag belt
    bbel_id: Mapped[Optional[str]]
    bbel_id_prev: Mapped[Optional[str]]
    bbel_start: Mapped[Optional[datetime]]
    bbel_start_et: Mapped[Optional[datetime]]
    bbel_end: Mapped[Optional[datetime]]
    # schedule
    sked_local: Mapped[datetime]
    sked_other: Mapped[datetime]
    # landing / takeoff
    at_local: Mapped[Optional[datetime]]
    at_local_et: Mapped[Optional[datetime]]
    at_other: Mapped[Optional[datetime]]
    at_other_et: Mapped[Optional[datetime]]
    takeoff_et: Mapped[Optional[datetime]]
    # departure / arrival to pk
    otpr: Mapped[Optional[datetime]]
    prb: Mapped[Optional[datetime]]
    # status
    status_id: Mapped[Optional[int]]
    status_code: Mapped[Optional[int]]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    company = relationship('CompanyModel', lazy='joined')
    aircraft = relationship('AircraftModel', lazy='joined')
    mar1 = relationship('AirportModel', lazy='joined', primaryjoin="FlightModel.mar1_id == AirportModel.id")
    mar2 = relationship('AirportModel', lazy='joined', primaryjoin="FlightModel.mar2_id == AirportModel.id")
    mar3 = relationship('AirportModel', lazy='joined', primaryjoin="FlightModel.mar3_id == AirportModel.id")
    mar4 = relationship('AirportModel', lazy='joined', primaryjoin="FlightModel.mar4_id == AirportModel.id")
    mar5 = relationship('AirportModel', lazy='joined', primaryjoin="FlightModel.mar5_id == AirportModel.id")
