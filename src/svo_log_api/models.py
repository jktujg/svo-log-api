from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .field_types import created_at, updated_at, Direction


class AircraftModel(Base):
    __tablename__ = 'aircrafts'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[Optional[int]] = mapped_column(unique=True, nullable=True)
    name: Mapped[Optional[str]]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    flights: Mapped[list['FlightModel']] = relationship(back_populates='aircraft')


class CountryModel(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    region: Mapped[Optional[str]] = None

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    cities: Mapped[list['CityModel']] = relationship(back_populates='country')


class CityModel(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    name_ru: Mapped[str] = mapped_column(unique=True)
    timezone: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id', ondelete='set null'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    country: Mapped['CountryModel'] = relationship(back_populates='cities', lazy='joined')
    airports: Mapped[list['AirportModel']] = relationship(back_populates='city')


class AirportModel(Base):
    __tablename__ = 'airports'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[int] = mapped_column(unique=False)
    iata: Mapped[str] = mapped_column(String(3), unique=True)
    icao: Mapped[str] = mapped_column(String(4), unique=False)
    code_ru: Mapped[Optional[str]] = mapped_column(String(3))
    name: Mapped[str]
    name_ru: Mapped[str]
    lat: Mapped[Optional[float]] = mapped_column(DECIMAL(9, 6))
    long: Mapped[Optional[float]] = mapped_column(DECIMAL(9, 6))
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete='set null'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    city: Mapped['CityModel'] = relationship(back_populates='airports', lazy='joined')


class CompanyModel(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    iata: Mapped[str] = mapped_column(String(2), unique=True)
    name: Mapped[Optional[str]]
    url_buy: Mapped[Optional[str]]
    url_register: Mapped[Optional[str]]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    flights: Mapped[list['FlightModel']] = relationship(back_populates='company')


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
    sked_local: Mapped[Optional[datetime]]
    sked_other: Mapped[Optional[datetime]]
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

    company: Mapped['CompanyModel'] = relationship(lazy='joined', back_populates='flights')
    aircraft: Mapped['AircraftModel'] = relationship(lazy='joined', back_populates='flights')
    mar1: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar1_id == AirportModel.id", backref='mar1_flights')
    mar2: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar2_id == AirportModel.id", backref='mar2_flights')
    mar3: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar3_id == AirportModel.id", backref='mar3_flights')
    mar4: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar4_id == AirportModel.id", backref='mar4_flights')
    mar5: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar5_id == AirportModel.id", backref='mar5_flights')
