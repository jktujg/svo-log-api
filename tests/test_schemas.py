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
        valid_aircraft = payloads.AircraftPayload().model_dump(by_alias=True)
        self.assertDictEqual(AircraftSchema(**valid_aircraft).model_dump(by_alias=True), valid_aircraft)

    def test_valid_country_model(self):
        valid_country = payloads.CountryPayload().model_dump(by_alias=True)
        self.assertDictEqual(CountrySchema(**valid_country).model_dump(by_alias=True), valid_country)

    def test_valid_airport_model(self):
        valid_airport = payloads.AirportPayload().model_dump(by_alias=True)
        self.assertDictEqual(AirportSchema(**valid_airport).model_dump(by_alias=True), valid_airport)

    def test_valid_company_model(self):
        valid_company = payloads.CompanyPayload(code='ala').model_dump(by_alias=True)
        self.assertDictEqual(CompanySchema(**valid_company).model_dump(by_alias=True), valid_company)

    def test_valid_flight_model(self):
        valid_flight = payloads.FlightPayload().model_dump(by_alias=True)
        self.assertDictEqual(FlightSchema(**valid_flight).model_dump(by_alias=True), valid_flight)