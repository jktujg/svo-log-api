from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..models import Base
from .fields import Direction
from ..fields import created_at, updated_at


class AircraftModel(Base):
    __tablename__ = 'aircrafts'

    name: Mapped[str] = mapped_column(primary_key=True)
    orig_id: Mapped[Optional[int]] = mapped_column()

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    flights: Mapped[list['FlightModel']] = relationship(back_populates='aircraft', lazy='noload')


class CountryModel(Base):
    __tablename__ = 'countries'

    name: Mapped[str] = mapped_column(primary_key=True)
    region: Mapped[Optional[str]] = None

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    cities: Mapped[list['CityModel']] = relationship(back_populates='country', lazy='noload')


class CityModel(Base):
    __tablename__ = 'cities'

    name: Mapped[str] = mapped_column(primary_key=True)
    name_ru: Mapped[str]
    timezone: Mapped[str]
    country_name: Mapped[str] = mapped_column(ForeignKey('countries.name', ondelete='set null'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    country: Mapped['CountryModel'] = relationship(back_populates='cities', lazy='joined')
    airports: Mapped[list['AirportModel']] = relationship(back_populates='city', lazy='noload')


class AirportModel(Base):
    __tablename__ = 'airports'

    iata: Mapped[str] = mapped_column(String(3), primary_key=True)
    icao: Mapped[Optional[str]] = mapped_column(String(4))
    code_ru: Mapped[Optional[str]] = mapped_column(String(3))
    orig_id: Mapped[Optional[int]]
    name: Mapped[str]
    name_ru: Mapped[str]
    lat: Mapped[Optional[float]] = mapped_column(DECIMAL(9, 6))
    long: Mapped[Optional[float]] = mapped_column(DECIMAL(9, 6))
    city_name: Mapped[str] = mapped_column(ForeignKey('cities.name', ondelete='set null'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    city: Mapped['CityModel'] = relationship(back_populates='airports', lazy='joined')


class CompanyModel(Base):
    __tablename__ = 'companies'

    iata: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[Optional[str]]
    url_buy: Mapped[Optional[str]]
    url_register: Mapped[Optional[str]]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    flights: Mapped[list['FlightModel']] = relationship(back_populates='company', lazy='noload')


class FlightModel(Base):
    __tablename__ = 'flights'

    id: Mapped[int] = mapped_column(primary_key=True)
    orig_id: Mapped[int] = mapped_column(unique=True)

    mar1_iata: Mapped[str] = mapped_column(ForeignKey('airports.iata', ondelete='set null'), nullable=True)
    mar2_iata: Mapped[str] = mapped_column(ForeignKey('airports.iata', ondelete='set null'), nullable=True)
    mar3_iata: Mapped[str] = mapped_column(ForeignKey('airports.iata', ondelete='set null'), nullable=True)
    mar4_iata: Mapped[str] = mapped_column(ForeignKey('airports.iata', ondelete='set null'), nullable=True)
    mar5_iata: Mapped[str] = mapped_column(ForeignKey('airports.iata', ondelete='set null'), nullable=True)
    aircraft_name: Mapped[str] = mapped_column(ForeignKey('aircrafts.name', ondelete='set null'), nullable=True)
    company_iata: Mapped[str] = mapped_column(ForeignKey('companies.iata', ondelete='set null'))

    number: Mapped[str]
    direction: Mapped[Direction]
    date: Mapped[datetime]
    main_orig_id: Mapped[Optional[int]]
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
    mar1: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar1_iata == AirportModel.iata", backref='mar1_flights')
    mar2: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar2_iata == AirportModel.iata", backref='mar2_flights')
    mar3: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar3_iata == AirportModel.iata", backref='mar3_flights')
    mar4: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar4_iata == AirportModel.iata", backref='mar4_flights')
    mar5: Mapped[Optional['AirportModel']] = relationship(lazy='joined', primaryjoin="FlightModel.mar5_iata == AirportModel.iata", backref='mar5_flights')
    changelog: Mapped[list['FlightsChangelogModel'] | None] = relationship(back_populates='flight', order_by='desc(FlightsChangelogModel.created_at)', lazy='noload')


class FlightsChangelogModel(Base):
    __tablename__ = 'flights_changelog'

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey('flights.id', ondelete='set null'), index=True)
    field: Mapped[str]
    old_value: Mapped[Optional[str]]

    created_at: Mapped[created_at]

    flight: Mapped['FlightModel'] = relationship(back_populates='changelog', lazy='noload')
