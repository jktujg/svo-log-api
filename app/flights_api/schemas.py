from datetime import datetime, timedelta
from functools import wraps
from typing import Annotated, Sequence

import regex
from fastapi import HTTPException, status
from pydantic import (BaseModel,
                      Field,
                      AnyHttpUrl,
                      ConfigDict,
                      AliasChoices,
                      field_validator,
                      model_validator,
                      field_serializer,
                      AwareDatetime,
                      )

from . import patterns
from .fields import Direction
from .utils import check_timedelta


@wraps(Field)
def QueryField(*a, **kw):
    field = Field(*a, **kw)
    alias = field.serialization_alias
    if alias is not None and regex.fullmatch(patterns.relation_alias, alias) is None:
        raise ValueError(f'Serialization {alias=} does not match pattern="{patterns.relation_alias}"')
    return field


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )


class EmptySchema(BaseModel):
    pass


class PagingSchema(BaseModel):
    page: int = Field(0, ge=0, description='Starts with 0')
    limit: int = Field(100, ge=1, le=100)

    def get_page(self, arr: Sequence):
        start_index = self.page * self.limit
        end_index = start_index + self.limit

        return arr[start_index: end_index]


class PagedResponseSchema(BaseSchema):
    items: list
    count: int
    total: int
    page: int
    total_pages: int


class ChangelogSchema(BaseModel):
    field: str
    old_value: str | None
    created_at: AwareDatetime


class AircraftSchema(BaseSchema):
    name: str
    orig_id: int | None = Field(validation_alias=AliasChoices('orig_id', 'id'))


class AircraftDBSchema(AircraftSchema):
    pass


class AircraftResponseSchema(AircraftSchema):
    pass


class AircraftPagedResponseSchema(PagedResponseSchema):
    items: list[AircraftResponseSchema]


class AircraftQuerySchema(BaseSchema):
    name: str | None = QueryField(None, serialization_alias='ilike::name')

    @field_validator('name', mode='after')
    @classmethod
    def add_wildcards(cls, field) -> str | None:
        return f'%{field}%' if field else None


class CountrySchema(BaseSchema):
    name: str
    region: str | None = None


class CountryDBSchema(CountrySchema):
    pass


class CountryResponseSchema(CountrySchema):
    pass


class CountryPagedResponseSchema(PagedResponseSchema):
    items: list[CountryResponseSchema]


class CitySchema(BaseSchema):
    name: str = Field(validation_alias=AliasChoices('name', 'name_en'))
    name_ru: str
    timezone: str
    country: CountrySchema


class CountryQuerySchema(BaseSchema):
    region: str | None = QueryField(None, serialization_alias='ilike::region')

    @field_validator('region', mode='after')
    @classmethod
    def add_wildcard(cls, field) -> str | None:
        return f'%{field}%' if field else None


class CityDBSchema(CitySchema):
    country: CountryDBSchema = Field(serialization_alias='country_name')

    @field_serializer('country', return_type=str)
    def serialize_country(self, country: CountrySchema, _info):
        return country.name


class CityResponseSchema(CitySchema):
    pass


class CityPagedResponseSchema(PagedResponseSchema):
    items: list[CityResponseSchema]


class CityQuerySchema(BaseSchema):
    timezone: str | None = QueryField(None, serialization_alias='ilike::timezone')
    region: str | None = QueryField(None, serialization_alias='ilike::CountryModel^region')
    country: str | None = QueryField(None, serialization_alias='ilike::CountryModel^name')
    name: str | None = QueryField(None, serialization_alias='ilike::name.name_ru')

    @field_validator('region', 'country', 'timezone', 'name', mode='after')
    @classmethod
    def add_wildcards(cls, field) -> str | None:
        return f'%{field}%' if field else None


class AirportSchema(BaseSchema):
    iata: str = Field(pattern=patterns.airport_iata)
    icao: str | None = Field(None, pattern=patterns.airport_icao)
    code_ru: str | None = Field(None, pattern=patterns.airport_code_ru)
    orig_id: int | None = Field(None,  validation_alias=AliasChoices('orig_id', 'id'))
    name: str
    name_ru: str
    lat: float | None = None
    long: float | None = None
    city: CitySchema


class AirportDBSchema(AirportSchema):
    city: CityDBSchema = Field(serialization_alias='city_name')

    @field_serializer('city', return_type=str)
    def serialize_city(self, city: CitySchema, _info):
        return city.name


class AirportResponseSchema(AirportSchema):
    pass


class AirportPagedResponseSchema(PagedResponseSchema):
    items: list[AirportResponseSchema]


class AirportQuerySchema(BaseSchema):
    city: str | None = QueryField(None, serialization_alias='ilike::CityModel^name.name_ru')
    timezone: str | None = QueryField(None, serialization_alias='ilike::CityModel^timezone')
    country: str | None = QueryField(None, serialization_alias='ilike::CityModel^CountryModel^name')
    region: str | None = QueryField(None, serialization_alias='ilike::CityModel^CountryModel^region')
    name: str | None = QueryField(None, serialization_alias='ilike::name.name_ru')
    date_start: AwareDatetime | None = QueryField(None, serialization_alias='ge@FlightModel^mar1_iata~mar2_iata~sked_local')
    date_end: AwareDatetime | None = QueryField(None, serialization_alias='le@FlightModel^mar1_iata~mar2_iata~sked_local')
    company : str | None = QueryField(None, serialization_alias='eq@FlightModel^mar1_iata~mar2_iata~company_iata', pattern=patterns.company_iata)
    direction: Direction | None = QueryField(None, serialization_alias='eq@FlightModel^mar1_iata~mar2_iata~direction')

    @field_validator('city', 'country', 'region', 'name', 'timezone', mode='after')
    @classmethod
    def add_wildcards(cls, field: str) -> str | None:
        return f'%{field}%' if field else None

    @model_validator(mode='after')
    def valitate_model(self):
        check_timedelta(self)
        if self.date_start is None or self.date_end is None:
            if self.company is not None or self.direction is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='date_start and date_end must be provided if airport or direction in use'
                )


class CompanySchema(BaseSchema):
    iata: str = Field(pattern=patterns.company_iata, validation_alias=AliasChoices('iata', 'code'))
    name: str | None = None
    url_buy: Annotated[str, AnyHttpUrl] | None = None
    url_register: Annotated[str, AnyHttpUrl] | None = None


class CompanyDBSchema(CompanySchema):
    pass


class CompanyResponseSchema(CompanySchema):
    pass


class CompanyQuerySchema(BaseSchema):
    name: str | None = QueryField(None, serialization_alias='ilike::name')
    date_start: AwareDatetime | None = QueryField(None, serialization_alias='ge@FlightModel^sked_local')
    date_end: AwareDatetime | None = QueryField(None, serialization_alias='le@FlightModel^sked_local')
    airport: str | None = QueryField(None, serialization_alias='eq@FlightModel^mar1_iata.mar2_iata', pattern=patterns.airport_iata)
    direction: Direction | None = QueryField(None, serialization_alias='eq@FlightModel^direction')

    @field_validator('name', mode='after')
    @classmethod
    def add_wildcard(cls, field) -> str | None:
        return f'%{field}%' if field else None

    @model_validator(mode='after')
    def valitate_model(self):
        check_timedelta(self)
        if self.date_start is None or self.date_end is None:
            if self.airport is not None or self.direction is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='date_start and date_end must be provided if airport or direction in use'
                )


class CompanyPagedResponseSchema(PagedResponseSchema):
    items: list[CompanyResponseSchema]


class FlightSchema(BaseSchema):
    orig_id: int = Field(validation_alias=AliasChoices('orig_id', 'id'))
    company: CompanySchema
    mar1: AirportSchema | None = None
    mar2: AirportSchema | None = None
    mar3: AirportSchema | None = None
    mar4: AirportSchema | None = None
    mar5: AirportSchema | None = None
    aircraft: AircraftSchema
    direction: Direction
    number: str
    date: AwareDatetime
    main_orig_id: int | None = Field(None, validation_alias=AliasChoices('main_orig_id', 'main_id'))
    way_time: int | None = None
    # check-in
    chin_start: AwareDatetime | None = None
    chin_end: AwareDatetime | None = None
    chin_start_et: AwareDatetime | None = None
    chin_end_et: AwareDatetime | None = None
    chin_id: str | None = None
    # boarding
    boarding_start: AwareDatetime | None = None
    boarding_end: AwareDatetime | None = None
    gate_id: str | None = None
    gate_id_prev: str | None = None
    # terminal
    term_local: str | None = None
    term_local_prev: str | None = None
    # bag belt
    bbel_id: str | None = None
    bbel_id_prev: str | None = None
    bbel_start: AwareDatetime | None = None
    bbel_start_et: AwareDatetime | None = None
    bbel_end: AwareDatetime | None = None
    # schedule
    sked_local: AwareDatetime | None = None
    sked_other: AwareDatetime | None = None
    # landing / takeoff
    at_local: AwareDatetime | None = None
    at_local_et: AwareDatetime | None = None
    at_other: AwareDatetime | None = None
    at_other_et: AwareDatetime | None = None
    takeoff_et: AwareDatetime | None = None
    # departure / arrival to pk
    otpr: AwareDatetime | None = None
    prb: AwareDatetime | None = None
    # status
    status_id: int | None = None
    status_code: int | None = None


class FlightDBSchema(FlightSchema):
    company: CompanyDBSchema = Field(serialization_alias='company_iata')
    mar1: AirportDBSchema | None = Field(None, serialization_alias='mar1_iata')
    mar2: AirportDBSchema | None = Field(None, serialization_alias='mar2_iata')
    mar3: AirportDBSchema | None = Field(None, serialization_alias='mar3_iata')
    mar4: AirportDBSchema | None = Field(None, serialization_alias='mar4_iata')
    mar5: AirportDBSchema | None = Field(None, serialization_alias='mar5_iata')
    aircraft: AircraftDBSchema = Field(serialization_alias='aircraft_name')

    @field_serializer('company', 'mar1', 'mar2', 'mar3', 'mar4', 'mar5', when_used='unless-none', return_type=str)
    def serialize_iata(self, schema, _info):
        return schema.iata

    @field_serializer('aircraft', return_type=str)
    def serialize_name(self, aircraft: AircraftSchema, _info):
        return aircraft.name


class FlightResponseSchema(FlightSchema):
    id: int
    changelog: list['ChangelogSchema'] | None = Field(default_factory=list)
    created_at: AwareDatetime
    updated_at: AwareDatetime


class FlightPagedResponseSchema(PagedResponseSchema):
    items: list[FlightResponseSchema]


class FlightQuerySchema(BaseSchema):
    date_start: AwareDatetime = QueryField(serialization_alias='ge@sked_local')
    date_end: AwareDatetime = QueryField(serialization_alias='le@sked_local')
    direction: Direction | None = None

    company: str | None = QueryField(None, pattern=patterns.company_iata_many, description='iata code', serialization_alias='in_::CompanyModel^iata')
    gate_id: str | None = None
    destination: str | None = QueryField(None, pattern=patterns.airport_iata_many, description='other airport', serialization_alias='in_::mar1_iata.mar2_iata')
    term_local: str | None = None
    number: str | None = None

    @field_validator('date_start', 'date_end', mode='after')
    @classmethod
    def up_to_minute(cls, date: datetime):
        if date is not None:
            return date.replace(second=0, microsecond=0) + timedelta(minutes=1)

    @field_validator('company', 'destination', mode='after')
    @classmethod
    def _split_iata(cls, iata: str | None) -> list[str] | None:
        if iata is not None:
            return iata.split(',')

    @model_validator(mode='after')
    def validate_model(self):
        check_timedelta(self)
        return self
