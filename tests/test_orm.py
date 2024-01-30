from src.svo_log_api import schemas
from src.svo_log_api.queries.orm import SyncOrm

from . import payloads
from .fixtures import DatabaseTestCase


class TestModels(DatabaseTestCase):
    def test_aircrafts_upsert(self):
        aircraft_1 = payloads.AircraftPayload(id=1, name='Boeing-777')
        aircraft_2 = payloads.AircraftPayload(id=1, name='SU-9')

        result_1 = SyncOrm.upsert_aircrafts(self.conn, [aircraft_1])
        result_2 = SyncOrm.upsert_aircrafts(self.conn, [aircraft_2])

        self.assertEqual(result_2[0].name, aircraft_2.name)

    def test_countries_upsert(self):
        country_1 = payloads.CountryPayload(name='Russia', region='DOMESTIC')
        country_2 = payloads.CountryPayload(name='Russia', region='INTERNATIONAL')

        result_1 = SyncOrm.upsert_countries(self.conn, [country_1])
        result_2 = SyncOrm.upsert_countries(self.conn, [country_2])

        self.assertEqual(result_2[0].region, country_2.region)

    def test_airports_upsert(self):
        airport_1 = payloads.AirportPayload(code_ru='OLD')
        airport_2 = payloads.AirportPayload(code_ru='NEW')

        result_1 = SyncOrm.upsert_airports(self.conn, [airport_1])
        result_2 = SyncOrm.upsert_airports(self.conn, [airport_2])

        self.assertEqual(result_2[0].code_ru, airport_2.code_ru)

    def test_companies_upsert(self):
        company_1 = payloads.CompanyPayload(iata='aa', name='old')
        company_2 = payloads.CompanyPayload(iata='aa', name='new')

        result_1 = SyncOrm.upsert_companies(self.conn, [company_1])
        result_2 = SyncOrm.upsert_companies(self.conn, [company_2])

        self.assertEqual(result_2[0].name, company_2.name)









