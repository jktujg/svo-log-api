from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from src.svo_log_api.config.config import settings
from src.svo_log_api import models
from src.svo_log_api import schemas
from src.svo_log_api.queries.orm import SyncOrm

from .fixtures import DatabaseTestCase


class TestModels(DatabaseTestCase):
    def test_aircrafts_upsert(self):
        aircraft_1 = schemas.AircraftSchema(id=1, name='Boeing-777')
        aircraft_2 = schemas.AircraftSchema(id=1, name='SU-9')

        result_1 = SyncOrm.upsert_aircrafts(self.conn, [aircraft_1])
        result_2 = SyncOrm.upsert_aircrafts(self.conn, [aircraft_2])

        self.assertEqual(result_2[0].name, aircraft_2.name)

    def test_countries_upsert(self):
        country_1 = schemas.CountrySchema(name='Russia', region='DOMESTIC')
        country_2 = schemas.CountrySchema(name='Russia', region='INTERNATIONAL')

        result_1 = SyncOrm.upsert_countries(self.conn, [country_1])
        result_2 = SyncOrm.upsert_countries(self.conn, [country_2])

        self.assertEqual(result_2[0].region, country_2.region)

    def test_airports_upsert(self):
        airport_1 = schemas.AirportSchema(
            id=439,
            iata='VRA',
            icao='MUVR',
            code_ru='ВРА',
            name='Хуан\xa0Гуальберто\xa0Гомес',
            name_ru='Хуан\xa0Гуальберто\xa0Гомес',
            country=dict(name='Russia', region='DOMESTIC'),
            city_ru='Варадеро',
            city_en='Varadero',
            lat=23.039896,
            long=-81.436943,
            timezone='America/Havana',
        )

        airport_2 = schemas.AirportSchema(
            id=439,
            iata='VRA',
            icao='MUVR',
            code_ru='ДЕР',
            name='Хуан\xa0Гуальберто\xa0Гомес',
            name_ru='Хуан\xa0Гуальберто\xa0Гомес',
            country=dict(name='Russia', region='DOMESTIC'),
            city_ru='Варадеро',
            city_en='Varadero',
            lat=23.039896,
            long=-81.436943,
            timezone='America/Havana',
        )

        result_1 = SyncOrm.upsert_airports(self.conn, [airport_1])
        result_2 = SyncOrm.upsert_airports(self.conn, [airport_2])

        self.assertEqual(result_2[0].code_ru, airport_2.code_ru)

        self.engine.echo = False









