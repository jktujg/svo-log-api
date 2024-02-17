from src.svo_log_api.flights_api import models

from tests.test_flight_api import payloads
from tests.fixtures import DatabaseTestCase


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
        valid_city = models.CityModel(**payloads.CityPayload(country=valid_country).model_dump())
        valid_schema = payloads.AirportPayload(city=valid_city).model_dump()
        airport = models.AirportModel(**valid_schema)
        self.conn.add(airport)
        self.conn.commit()

    def test_company_model_add(self):
        valid_schema = payloads.CompanyPayload().model_dump()
        company = models.CompanyModel(**valid_schema)
        self.conn.add(company)
        self.conn.commit()

    def test_flight_model_add(self):
        valid_company = models.CompanyModel(**payloads.CompanyPayload().model_dump())
        valid_aircraft = models.AircraftModel(**payloads.AircraftPayload().model_dump())
        valid_country_1 = models.CountryModel(**payloads.CountryPayload(name='Russia').model_dump())
        valid_country_2 = models.CountryModel(**payloads.CountryPayload(name='Israel').model_dump())
        valid_city_1 = models.CityModel(**payloads.CityPayload(country=valid_country_1, name_en='Moscow', name_ru='Москва').model_dump())
        valid_city_2 = models.CityModel(**payloads.CityPayload(country=valid_country_2, name_en='Tel Aviv', name_ru='Тель Авив').model_dump())
        valid_mar1 = models.AirportModel(**payloads.AirportPayload(city=valid_city_1, id=1, iata='SVO', icao='UUEE').model_dump())
        valid_mar2 = models.AirportModel(**payloads.AirportPayload(city=valid_city_2, id=2, iata='TLV', icao='TTLV').model_dump())

        valid_flight_schema = payloads.FlightPayload(
            company=valid_company,
            aircraft=valid_aircraft,
            mar1=valid_mar1,
            mar2=valid_mar2,
        ).model_dump()

        flight = models.FlightModel(**valid_flight_schema)
        self.conn.add(flight)
        self.conn.commit()
        self.conn.refresh(flight)

        self.assertEqual(flight.mar1.iata, 'SVO')
        self.assertEqual(flight.mar2.iata, 'TLV')

    def test_city_model_add(self):
        valid_country = payloads.CountryPayload().model_dump()
        country = models.CountryModel(**valid_country)
        valid_city = payloads.CityPayload(country=country).model_dump()
        city = models.CityModel(**valid_city)

        self.conn.add(city)
        self.conn.commit()
