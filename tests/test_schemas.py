from unittest import TestCase
from src.svo_log_api.schemas import (
    AircraftSchema,
    CountrySchema,
    AirportSchema,
    CompanySchema,
    FlightSchema,
)

from . import payloads


class TestSchemas(TestCase):

    def test_valid_aircraft_model(self):
        AircraftSchema.model_validate(payloads.AircraftPayload().model_dump(by_alias=True))

    def test_valid_country_model(self):
        CountrySchema.model_validate(payloads.CountryPayload().model_dump(by_alias=True))

    def test_valid_airport_model(self):
        AirportSchema.model_validate(payloads.AirportPayload().model_dump(by_alias=True))

    def test_valid_company_model(self):
        CompanySchema.model_validate(payloads.CompanyPayload().model_dump(by_alias=True))

    def test_valid_flight_model(self):
        FlightSchema.model_validate(payloads.FlightPayload().model_dump(by_alias=True))