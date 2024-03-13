from datetime import datetime, timedelta
from typing import Annotated
from pydantic import (BaseModel,
                      Field,
                      AnyHttpUrl,
                      ConfigDict,
                      AliasChoices,
                      field_validator,
                      )
from .field_types import Direction

#todo add alias generators for serializing by alias in camel case style
class BaseEntity(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )


class AircraftSchema(BaseEntity):
    name: str
    orig_id: int | None = Field(validation_alias=AliasChoices('orig_id', 'id'))


class CountrySchema(BaseEntity):
    name: str
    region: str | None = None


class CitySchema(BaseEntity):
    name: str = Field(validation_alias=AliasChoices('name', 'name_en'))
    name_ru: str
    timezone: str
    country: CountrySchema


class AirportSchema(BaseEntity):
    iata: str = Field(pattern='^[A-Z]{3}$')
    icao: str | None = Field(None, pattern='^[A-Z]{4}$')
    code_ru: str | None = Field(None, pattern=r'^([А-Я]{3})|.{0}$')
    orig_id: int | None = Field(None,  validation_alias=AliasChoices('orig_id', 'id'))
    name: str
    name_ru: str
    lat: float | None = None
    long: float | None = None
    city: CitySchema

#todo change company to airline
class CompanySchema(BaseEntity):
    iata: str = Field(pattern=r'^\w{2}$', validation_alias=AliasChoices('iata', 'code'))
    name: str | None = None
    url_buy: Annotated[str, AnyHttpUrl] | None = None
    url_register: Annotated[str, AnyHttpUrl] | None = None


class FlightSchema(BaseEntity):
    orig_id: int = Field(validation_alias=AliasChoices('orig_id', 'id'))
    direction: Direction
    company: CompanySchema
    number: str
    date: datetime
    mar1: AirportSchema | None = None
    mar2: AirportSchema | None = None
    mar3: AirportSchema | None = None
    mar4: AirportSchema | None = None
    mar5: AirportSchema | None = None
    aircraft: AircraftSchema
    main_orig_id: int | None = Field(None, validation_alias=AliasChoices('main_orig_id', 'main_id'))
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


class ChangelogFlightSchema(BaseModel):
    field: str
    old_value: str | None
    created_at: datetime


class FlightResponseSchema(FlightSchema):
    id: int
    changelog: list[ChangelogFlightSchema] | None = Field(default_factory=list)


class FlightResponseContainer(BaseModel):
    flights: list[FlightResponseSchema]
    count: int
    total: int
    page: int
    total_pages: int = Field()


class FlightsGetParamsSchema(BaseModel):
    date_start: datetime = Field(description='departure or landing')
    date_end: datetime = Field(description='departure or landing')
    direction: Direction

    company: str | None = Field(None, pattern=r'^\w{2}$', description='iata code')
    gate_id: str | None = None
    destination: str | None = Field(None,  pattern='^[A-Z]{3}$', description='other airport')

    @field_validator('date_start', 'date_end', mode='after')
    @classmethod
    def up_to_minute(cls, date: datetime):
        """ For caching """
        if date is not None:
            return date.replace(second=0, microsecond=0) + timedelta(minutes=1)


class PagingSchema(BaseModel):
    page: int = Field(0, ge=0, description='Starts with 0')
    limit: int = Field(100, ge=1, le=100)
