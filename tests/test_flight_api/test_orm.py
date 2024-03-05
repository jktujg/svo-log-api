from sqlalchemy import select
from datetime import datetime, timedelta

from src.svo_log_api.flights_api.queries.orm import SyncOrm
from src.svo_log_api.flights_api import models, schemas

from tests.test_flight_api import payloads
from tests.fixtures import AppTestCase


class TestModels(AppTestCase):
    def _upsert_flights_from_dict(self, flights: list[dict]):
        """ Inserts flights one by one to ensure id sequence """
        models = []
        for f in flights:
            model = SyncOrm.upsert_flights(
                conn=self.conn,
                data=[schemas.FlightSchema(**payloads.FlightPayload(**f).model_dump(by_alias=True))]
            )
            models.append(model)
        return models

    def test_aircrafts_upsert(self):
        aircraft_1 = payloads.AircraftPayload(name='Boeing-777', id=1)
        aircraft_2 = payloads.AircraftPayload(name='Boeing-777', id=2)

        result_1 = SyncOrm.upsert_aircrafts(self.conn, [aircraft_1])
        result_2 = SyncOrm.upsert_aircrafts(self.conn, [aircraft_2])

        self.assertEqual(result_2[0].orig_id, aircraft_2.orig_id)

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
        self.assertEqual(changelog[0].old_value, flight_1.chin_id)

    def test_cities_upsert(self):
        city_1 = payloads.CityPayload(name_en='Moscow', timezone='A')
        city_2 = payloads.CityPayload(name_en='Moscow', timezone='B')

        result_1 = SyncOrm.upsert_cities(self.conn, [city_1])
        result_2 = SyncOrm.upsert_cities(self.conn, [city_2])

        self.assertEqual(result_2[0].timezone, 'B')

    def test_get_flights_ids_required_params(self):
        now = datetime.now()
        flights = [
            dict(schemas.CompanySchema(iata='SU'), direction='arrival', id=1, sked_local=now - timedelta(days=10)),
            dict(company=schemas.CompanySchema(iata='N4'), direction='arrival', id=2, sked_local=now),
            dict(company=schemas.CompanySchema(iata='N4'), direction='departure', id=3, sked_local=now),
            dict(company=schemas.CompanySchema(iata='U2'), direction='arrival', id=4, sked_local=now + timedelta(days=10))
        ]
        self._upsert_flights_from_dict(flights)

        selected_flight_ids = SyncOrm.get_flight_ids(conn=self.conn, params=schemas.FlightsGetParamsSchema(
            direction='arrival',
            date_start=datetime.now() - timedelta(hours=1),
            date_end=datetime.now() + timedelta(hours=2),
        ))

        self.assertListEqual(selected_flight_ids, [2])

    def test_get_flights_ids_company(self):
        flights = [
            dict(company=schemas.CompanySchema(iata='SU'), direction='arrival', id=1),
            dict(company=schemas.CompanySchema(iata='N4'), direction='arrival', id=2),
        ]
        self._upsert_flights_from_dict(flights)
        query_flights = SyncOrm.get_flight_ids(conn=self.conn, params=schemas.FlightsGetParamsSchema(
            company='SU',
            direction='arrival',
            date_start=datetime.now() - timedelta(days=10000),
            date_end=datetime.now()
        ))

        self.assertListEqual(query_flights, [1])

    def test_get_flights_ids_gate_id(self):
        flights = [
            dict(direction='arrival', id=1, gate_id='c1'),
            dict(direction='arrival', id=2, gate_id='d5')
        ]
        self._upsert_flights_from_dict(flights)
        query_flights = SyncOrm.get_flight_ids(conn=self.conn, params=schemas.FlightsGetParamsSchema(
            gate_id='c1',
            direction='arrival',
            date_start=datetime.now() - timedelta(days=10000),
            date_end=datetime.now()
        ))

        self.assertListEqual(query_flights, [1])

    def test_get_flights_ids_destination(self):
        flights = [
            dict(direction='arrival', id=1, mar1=payloads.AirportPayload(iata='KGF')),
            dict(direction='departure', id=2, mar2=payloads.AirportPayload(iata='LAX'))
        ]
        self._upsert_flights_from_dict(flights)
        flight_kgf = SyncOrm.get_flight_ids(conn=self.conn, params=schemas.FlightsGetParamsSchema(
            destination='KGF',
            direction='arrival',
            date_start=datetime.now() - timedelta(days=10000),
            date_end=datetime.now()
        ))
        flight_lax = SyncOrm.get_flight_ids(conn=self.conn, params=schemas.FlightsGetParamsSchema(
            destination='LAX',
            direction='departure',
            date_start=datetime.now() - timedelta(days=10000),
            date_end=datetime.now()
        ))

        self.assertListEqual(flight_kgf, [1])
        self.assertListEqual(flight_lax, [2])

    def test_get_flights_by_ids(self):
        flights = [
            dict(direction='arrival', id=1),
            dict(direction='departure', id=2, gate_id='old'),
            dict(direction='departure', id=2, gate_id='new'),
            dict(direction='departure', id=3),
        ]
        self._upsert_flights_from_dict(flights)
        flight_models = SyncOrm.get_flights_by_ids(conn=self.conn, ids=[1, 2, 5], changelog=False)

        self.assertEqual(len(flight_models), 2)
        self.assertListEqual(flight_models[1].changelog, [])

    def test_get_flights_by_ids_with_changelog(self):
        flights = [
            dict(direction='arrival', id=1, gate_id='old'),
            dict(direction='arrival', id=1, gate_id='new'),
        ]
        self._upsert_flights_from_dict(flights)
        flight_models = SyncOrm.get_flights_by_ids(conn=self.conn, ids=[1], changelog=True)

        self.assertEqual(flight_models[0].changelog[0].old_value, 'old')


