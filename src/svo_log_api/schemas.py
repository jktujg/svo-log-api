from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, AnyHttpUrl
from typing import Annotated


class BaseEntity(BaseModel):

    class Config:
        frozen = True


class AircraftModel(BaseEntity):
    orig_id: int | None = Field(alias='id')
    name: str | None = None


class CountryModel(BaseEntity):
    name: str
    region: str


class AirportModel(BaseEntity):
    orig_id: int = Field(alias='id')
    iata: str = Field(pattern='[A-Z]{3}')
    icao: str = Field(pattern='[A-Z]{4}')
    code_ru: str | None = Field(pattern='[А-Я]{3}')
    name: str
    name_ru: str
    city_ru: str
    city_en: str
    lat: float | None = None
    long: float | None = None
    timezone: str | None = None
    country: CountryModel


class CompanyModel(BaseEntity):
    code: str = Field(pattern=r'\w{2}')
    name: str | None = None
    url_buy: Annotated[str, AnyHttpUrl] | None = None
    url_register: Annotated[str, AnyHttpUrl] | None = None


class Direction(Enum):
    arrival = 'arrival'
    departure = 'departure'


class FlightModel(BaseEntity):
    orig_id: int = Field(alias='id')
    direction: Annotated[str, Direction]
    company: CompanyModel
    number: int
    date: Annotated[str, datetime]
    mar1: AirportModel
    mar2: AirportModel
    mar3: AirportModel | None = None
    mar4: AirportModel | None = None
    mar5: AirportModel | None = None
    aircraft: AircraftModel
    main_id: int | None = None
    way_time: int | None = None
    # check-in
    chin_start: Annotated[str | None, datetime] = None
    chin_end: Annotated[str | None, datetime] = None
    chin_start_et: Annotated[str | None, datetime] = None
    chin_end_et: Annotated[str | None, datetime] = None
    chin_id: str | None = None
    # boarding
    boarding_start: Annotated[str | None, datetime] = None
    boarding_end: Annotated[str | None, datetime] = None
    gate_id: str | None = None
    gate_id_prev: str | None = None
    # terminal
    term_local: str | None = None
    term_local_prev: str | None = None
    # bag belt
    bbel_id: str | None = None
    bbel_id_prev: str | None = None
    bbel_start: Annotated[str | None, datetime] = None
    bbel_start_et: Annotated[str | None, datetime] = None
    bbel_end: Annotated[str | None, datetime] = None
    # schedule
    sked_local: Annotated[str, datetime]
    sked_other: Annotated[str, datetime]
    # landing / takeoff
    at_local: Annotated[str | None, datetime] = None
    at_local_et: Annotated[str | None, datetime] = None
    at_other: Annotated[str | None, datetime] = None
    at_other_et: Annotated[str | None, datetime] = None
    takeoff_et: Annotated[str | None, datetime] = None
    # departure / arrival to pk
    otpr: Annotated[str | None, datetime] = None
    prb: Annotated[str | None, datetime] = None
    # status
    status_id: int | None = None
    status_code: int | None = None

