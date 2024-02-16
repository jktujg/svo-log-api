from sqlalchemy import select

from src.svo_log_api import schemas
from src.svo_log_api.queries.orm import SyncOrm
from src.svo_log_api import models, schemas

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
        company_1 = payloads.CompanyPayload(name='old')
        company_2 = payloads.CompanyPayload(name='new')

        result_1 = SyncOrm.upsert_companies(self.conn, [company_1])
        result_2 = SyncOrm.upsert_companies(self.conn, [company_2])

        self.assertEqual(result_2[0].name, company_2.name)

    def test_flights_upsert(self):
        flight_1 = payloads.FlightPayload(id=1, chin_id='old')
        flight_2 = payloads.FlightPayload(id=1, chin_id='new')

        result1 = SyncOrm.upsert_flights(self.conn, [flight_1])
        result2 = SyncOrm.upsert_flights(self.conn, [flight_2])

        self.assertEqual(result2[0].orig_id, flight_1.orig_id)      # `orig_id` is aliased `id`
        self.assertEqual(result2[0].chin_id, flight_2.chin_id)

    def test_flights_upsert_changelog_update(self):
        # wrap payloads in original schemas because payloads skip validation and thus converting
        # (in this case str dates to datetime)
        flight_1 = schemas.FlightSchema(**payloads.FlightPayload(id=1, chin_id='old').model_dump(by_alias=True))
        flight_2 = schemas.FlightSchema(**payloads.FlightPayload(id=1, chin_id='new').model_dump(by_alias=True))

        result1 = SyncOrm.upsert_flights(self.conn, [flight_1])
        result2 = SyncOrm.upsert_flights(self.conn, [flight_2])

        query = select(models.FlightsChangelogModel).filter(models.FlightsChangelogModel.flight_id == 1)
        changelog = self.conn.execute(query).scalars().all()

        self.assertEqual(len(changelog), 1)
        self.assertEqual(changelog[0].field, 'chin_id')
        self.assertEqual(changelog[0].new_value, flight_2.chin_id)

        # self.assertListEqual([changelog.field, changelog.new_value], ['chin_id', flight_2.chin_id])

    def test_cities_upsert(self):
        city_1 = payloads.CityPayload(name_en='Moscow', timezone='A')
        city_2 = payloads.CityPayload(name_en='Moscow', timezone='B')

        result_1 = SyncOrm.upsert_cities(self.conn, [city_1])
        result_2 = SyncOrm.upsert_cities(self.conn, [city_2])

        self.assertEqual(result_2[0].timezone, 'B')
