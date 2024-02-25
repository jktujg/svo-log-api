from datetime import datetime
from pydantic import BaseModel, Field, AnyHttpUrl, ConfigDict
from typing import Annotated

from .field_types import Direction


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )


class AircraftSchema(BaseEntity):
    orig_id: int | None = Field(alias='id')
    name: str | None = None


class CountrySchema(BaseEntity):
    name: str
    region: str | None = None


class CitySchema(BaseEntity):
    name: str = Field(alias='name_en')
    name_ru: str
    timezone: str
    country: CountrySchema


class AirportSchema(BaseEntity):
    orig_id: int = Field(alias='id')
    iata: str = Field(pattern='^[A-Z]{3}$')
    icao: str = Field(pattern='^[A-Z]{4}$')
    code_ru: str | None = Field(pattern=r'^([А-Я]{3})|.{0}$')
    name: str
    name_ru: str
    lat: float | None = None
    long: float | None = None
    city: CitySchema


class CompanySchema(BaseEntity):
    iata: str = Field(pattern=r'^\w{2}$', alias='code')
    name: str | None = None
    url_buy: Annotated[str, AnyHttpUrl] | None = None
    url_register: Annotated[str, AnyHttpUrl] | None = None


class FlightSchema(BaseEntity):
    orig_id: int = Field(alias='id')
    direction: Direction
    company: CompanySchema
    number: int
    date: datetime
    mar1: AirportSchema | None = None
    mar2: AirportSchema | None = None
    mar3: AirportSchema | None = None
    mar4: AirportSchema | None = None
    mar5: AirportSchema | None = None
    aircraft: AircraftSchema
    main_id: int | None = None
    way_time: int | None = None
    # check-in
    chin_start: datetime | None = None
    chin_end: datetime | None = None
    chin_start_et: datetime | None = None
    chin_end_et: datetime | None = None
    chin_id: str | None = None
    # boarding
    boarding_start: datetime | None = None
    boarding_end: datetime | None = None
    gate_id: str | None = None
    gate_id_prev: str | None = None
    # terminal
    term_local: str | None = None
    term_local_prev: str | None = None
    # bag belt
    bbel_id: str | None = None
    bbel_id_prev: str | None = None
    bbel_start: datetime | None = None
    bbel_start_et: datetime | None = None
    bbel_end: datetime | None = None
    # schedule
    sked_local: datetime | None = None
    sked_other: datetime | None = None
    # landing / takeoff
    at_local: datetime | None = None
    at_local_et: datetime | None = None
    at_other: datetime | None = None
    at_other_et: datetime | None = None
    takeoff_et: datetime | None = None
    # departure / arrival to pk
    otpr: datetime | None = None
    prb: datetime | None = None
    # status
    status_id: int | None = None
    status_code: int | None = None

