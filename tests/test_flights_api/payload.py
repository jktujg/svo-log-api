from datetime import datetime, timedelta
from functools import partial
from random import randint, uniform, choice, randrange
from typing import Annotated, Callable, Literal

from pydantic import BaseModel, ConfigDict, Field, AnyHttpUrl

from tests.utils import random_string


class Payload(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True,
        frozen=True,
    )


random_string_factory = partial(random_string, n_upper=randint(1, 10), n_lower=randint(1, 20))


def random_url_factory(n: int) -> Callable[[], str]:
    def _url() -> str:
        return 'https://' + random_string(n_lower=n) + '.com'
    return _url


def random_dt_string(days_diff: int) -> Callable[[], str]:
    days_diff = max(1, days_diff)

    def _dt() -> str:
        now = datetime.now()
        prev = now - timedelta(days=days_diff)
        random_ts = randrange(int(prev.timestamp()), int(now.timestamp()))

        return datetime.fromtimestamp(random_ts).isoformat() + 'Z'

    return _dt


def dt_string(**delta_params) -> str:
    return (datetime.now() + timedelta(**delta_params)).isoformat() + 'Z'


class AircraftPayload(Payload):
    orig_id: int | None = Field(default_factory=partial(randint, 1, int(1e6)))
    name: str = Field(default_factory=random_string_factory)


def aircraft(**params):
    return AircraftPayload(**params).model_dump()


class CountryPayload(Payload):
    name: str = Field(default_factory=random_string_factory)
    region: str | None = Field(default_factory=random_string_factory)


def country(**params):
    return CountryPayload(**params).model_dump()


class CityPayload(Payload):
    name: str = Field(default_factory=random_string_factory)
    name_ru: str = Field(default_factory=random_string_factory)
    timezone: str = Field(default_factory=random_string_factory)
    country: dict = Field(default_factory=country)


def city(**params):
    return CityPayload(**params).model_dump()


class AirportPayload(Payload):
    iata: str = Field(default_factory=partial(random_string, n_upper=3))
    icao: str | None = Field(default_factory=partial(random_string, n_upper=4))
    code_ru: str | None = Field(default_factory=partial(random_string, n_upper=3))
    orig_id: int | None = Field(default_factory=partial(randint, int(1e6), int(1e9)))
    name: str = Field(default_factory=random_string_factory)
    name_ru: str = Field(default_factory=random_string_factory)
    lat: float | None = Field(default_factory=lambda: round(uniform(-90, 90), 6))
    long: float | None = Field(default_factory=lambda: round(uniform(-180, 180), 6))
    city: dict = Field(default_factory=city)


def airport(**params):
    return AirportPayload(**params).model_dump()


class CompanyPayload(Payload):
    iata: str = Field(default_factory=partial(random_string, n_upper=2))
    name: str | None = Field(default_factory=random_string_factory)
    url_buy: Annotated[str, AnyHttpUrl] | None = Field(default_factory=random_url_factory(20))
    url_register: Annotated[str, AnyHttpUrl] | None = Field(default_factory=random_url_factory(20))


def company(**params):
    return CompanyPayload(**params).model_dump()


class FlightPayload(Payload):
    orig_id: int = Field(default_factory=partial(randint, int(1e6), int(1e9)))
    company: dict = Field(default_factory=company)
    mar1: dict | None = Field(default_factory=airport)
    mar2: dict | None = Field(default_factory=airport)
    mar3: dict | None = None
    mar4: dict | None = None
    mar5: dict | None = None
    aircraft: dict = Field(default_factory=aircraft)
    direction: Literal['arrival', 'departure'] = Field(default_factory=partial(choice, ['arrival', 'departure']))
    number: str = Field(default_factory=partial(random_string, n_digit=9))
    date: str = Field(default_factory=random_dt_string(3))
    main_orig_id: int | None = None
    way_time: int | None = Field(default_factory=partial(randint, 1, 1000))
    # check-in
    chin_start: str | None = Field(default_factory=random_dt_string(3))
    chin_end: str | None = Field(default_factory=random_dt_string(3))
    chin_start_et: str | None = Field(default_factory=random_dt_string(3))
    chin_end_et: str | None = Field(default_factory=random_dt_string(3))
    chin_id: str | None = Field(default_factory=random_string_factory)
    # boarding
    boarding_start: str | None = Field(default_factory=random_dt_string(3))
    boarding_end: str | None = Field(default_factory=random_dt_string(3))
    gate_id: str | None = Field(default_factory=partial(random_string, n_digit=3, n_upper=1))
    gate_id_prev: str | None = Field(default_factory=partial(random_string, n_digit=3, n_upper=1))
    # terminal
    term_local: str | None = Field(default_factory=partial(random_string, n_upper=1))
    term_local_prev: str | None = Field(default_factory=partial(random_string, n_upper=1))
    # bag belt
    bbel_id: str | None = Field(default_factory=partial(random_string, n_digit=2, n_upper=1))
    bbel_id_prev: str | None = Field(default_factory=partial(random_string, n_digit=2, n_upper=1))
    bbel_start: str | None = Field(default_factory=random_dt_string(3))
    bbel_start_et: str | None = Field(default_factory=random_dt_string(3))
    bbel_end: str | None = Field(default_factory=random_dt_string(3))
    # schedule
    sked_local: str | None = Field(default_factory=random_dt_string(3))
    sked_other: str | None = Field(default_factory=random_dt_string(3))
    # landing / takeoff
    at_local: str | None = Field(default_factory=random_dt_string(3))
    at_local_et: str | None = Field(default_factory=random_dt_string(3))
    at_other: str | None = Field(default_factory=random_dt_string(3))
    at_other_et: str | None = Field(default_factory=random_dt_string(3))
    takeoff_et: str | None = Field(default_factory=random_dt_string(3))
    # departure / arrival to pk
    otpr: str | None = Field(default_factory=random_dt_string(3))
    prb: str | None = Field(default_factory=random_dt_string(3))
    # status
    status_id: int | None = Field(default_factory=partial(randint, 1, 1000))
    status_code: int | None = Field(default_factory=partial(randint, 1, 1000))


def flight(**params):
    return FlightPayload(**params).model_dump()
