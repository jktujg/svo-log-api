from typing import Any
from pydantic import BaseModel, SkipValidation, Field, ConfigDict


class Payload(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True,
        frozen=True,
    )


class AircraftPayload(Payload):
    orig_id: SkipValidation[Any] = Field(default=152, alias='id')
    name: SkipValidation[Any] = 'Airbus 333'


class CountryPayload(Payload):
    name: SkipValidation[Any] = 'Russia'
    region: SkipValidation[Any] = 'DOMESTIC'


class CityPayload(Payload):
    name: SkipValidation[Any] = Field(default='Moscow', alias='name_en')
    name_ru: SkipValidation[Any] = 'Москва'
    country: SkipValidation[Any] = CountryPayload()
    timezone: SkipValidation[Any] = 'America/Havana'


class AirportPayload(Payload):
    orig_id: SkipValidation[Any] = Field(default=439, alias='id')
    iata: SkipValidation[Any] = 'VRA'
    icao: SkipValidation[Any] = 'MUVR'
    code_ru: SkipValidation[Any] = 'ВРА'
    name: SkipValidation[Any] = 'Хуан\xa0Гуальберто\xa0Гомес'
    name_ru: SkipValidation[Any] = 'Хуан\xa0Гуальберто\xa0Гомес'
    city: SkipValidation[Any] = CityPayload()
    lat: SkipValidation[Any] = 23.039896
    long: SkipValidation[Any] = -81.436943


class CompanyPayload(Payload):
    name: SkipValidation[Any] = "Nordwind"
    iata: SkipValidation[Any] = Field(default='N4', alias='code')
    url_buy: SkipValidation[Any] = 'https://nordwindairlines.ru/'
    url_register: SkipValidation[Any] = 'https://airbook.nordwindairlines.ru/check-in/?lang=ru#search'


class FlightPayload(Payload):
    orig_id: SkipValidation[Any] = Field(default=8770878, alias='id')
    direction: SkipValidation[Any] = 'arrival'
    number: SkipValidation[Any] = '556'
    date: SkipValidation[Any] = '2023-12-19T00:00:00+03:00'
    mar1: SkipValidation[Any] = AirportPayload()
    takeoff_et: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    at_other_et: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    mar2: SkipValidation[Any] = AirportPayload()
    mar3: SkipValidation[Any] = None
    mar4: SkipValidation[Any] = None
    mar5: SkipValidation[Any] = None
    at_local: SkipValidation[Any] = '2023-12-20T04:27:02+03:00'
    term_local: SkipValidation[Any] = 'C'
    term_local_prev: SkipValidation[Any] = 'C'
    sked_local: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    at_local_et: SkipValidation[Any] = '2023-12-20T04:54:00+03:00'
    chin_id: SkipValidation[Any] = '312-315'
    chin_start: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    chin_end: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    gate_id: SkipValidation[Any] = '1a'
    gate_id_prev: SkipValidation[Any] = '12'
    boarding_start: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    boarding_end: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    bbel_id: SkipValidation[Any] = '1-2'
    bbel_id_prev: SkipValidation[Any] = '1-2'
    bbel_start: SkipValidation[Any] = '2023-12-20T04:56:00+03:00'
    bbel_end: SkipValidation[Any] = '2023-12-20T05:25:00+03:00'
    main_orig_id: SkipValidation[Any] = Field(default=8770879, alias='main_id')
    status_code: SkipValidation[Any] = 12
    status_id: SkipValidation[Any] = 70
    aircraft: SkipValidation[Any] = AircraftPayload()
    chin_start_et: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    chin_end_et: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    bbel_start_et: SkipValidation[Any] = '2023-12-20T04:56:00+03:00'
    sked_other: SkipValidation[Any] = '2023-12-19T05:00:00+03:00'
    at_other: SkipValidation[Any] = '2023-12-19T16:00:00+03:00'
    way_time: SkipValidation[Any] = 693
    otpr: SkipValidation[Any] = '2023-12-19T18:55:00+03:00'
    prb: SkipValidation[Any] = None
    company: SkipValidation[Any] = CompanyPayload()
