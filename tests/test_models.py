from unittest import TestCase
from src.svo_log_api import models

from . import payloads
from .fixtures import DatabaseTestCase


class TestModels(DatabaseTestCase):
    def test_aircraft_model_add(self):
        valid_schema = payloads.AircraftPayload().model_dump()
        aircraft = models.AircraftModel(**valid_schema)
        self.conn.add(aircraft)
        self.conn.commit()

    def test_country_model_add(self):
        valid_schema = payloads.CountryPayload().model_dump()
        country = models.CountryModel(**valid_schema)
        self.conn.add(country)
        self.conn.commit()

    def test_airport_model_add(self):
        valid_country = models.CountryModel(**payloads.CountryPayload().model_dump())
        valid_schema = payloads.AirportPayload(country=valid_country).model_dump()
        airport = models.AirportModel(**valid_schema)
        self.conn.add(airport)
        self.conn.commit()

    def test_company_model_add(self):
        valid_schema = payloads.CompanyPayload().model_dump()
        company = models.CompanyModel(**valid_schema)
        self.conn.add(company)
        self.conn.commit()