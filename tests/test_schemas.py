from unittest import TestCase
from src.svo_log_api.schemas import (
    AircraftSchema,
    CountrySchema,
    AirportSchema,
    CompanySchema,
    FlightSchema,
)


class TestSchemas(TestCase):

    def test_valid_aircraft_model(self):
        valid_aircraft = dict(id=152, name='aircraft name')
        self.assertDictEqual(AircraftSchema(**valid_aircraft).model_dump(by_alias=True), valid_aircraft)

    def test_valid_country_model(self):
        valid_country = dict(name='Russia', region='DOMESTIC')
        self.assertDictEqual(CountrySchema(**valid_country).model_dump(by_alias=True), valid_country)

    def test_valid_airport_model(self):
        valid_airport = dict(
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
        self.assertDictEqual(AirportSchema(**valid_airport).model_dump(by_alias=True), valid_airport)

    def test_valid_company_model(self):
        valid_company = dict(
            name='Nordwind Airlines',
            code='N4',
            url_buy='https://nordwindairlines.ru/',
            url_register='https://airbook.nordwindairlines.ru/check-in/?lang=ru#search',
        )
        self.assertDictEqual(CompanySchema(**valid_company).model_dump(by_alias=True), valid_company)

    def test_valid_flight_model(self):
        valid_flight = dict(
            id=8770878,
            direction='arrival',
            number=556,
            date='2023-12-19T00:00:00+03:00',
            mar1=dict(
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
            ),
            takeoff_et='2023-12-19T18:55:00+03:00',
            at_other_et='2023-12-19T18:55:00+03:00',
            mar2=dict(
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
            ),
            mar3=None,
            mar4=None,
            mar5=None,
            at_local='2023-12-20T04:27:02+03:00',
            term_local='C',
            term_local_prev='C',
            sked_local='2023-12-19T18:55:00+03:00',
            at_local_et='2023-12-20T04:54:00+03:00',
            chin_id='312-315',
            chin_start='2023-12-19T18:55:00+03:00',
            chin_end='2023-12-19T18:55:00+03:00',
            gate_id='1a',
            gate_id_prev='12',
            boarding_start='2023-12-19T18:55:00+03:00',
            boarding_end='2023-12-19T18:55:00+03:00',
            bbel_id='1-2',
            bbel_id_prev='1-2',
            bbel_start='2023-12-20T04:56:00+03:00',
            bbel_end='2023-12-20T05:25:00+03:00',
            main_id=8770879,
            status_code=12,
            status_id=70,
            aircraft=dict(id=152, name='aircraft name'),
            chin_start_et='2023-12-19T18:55:00+03:00',
            chin_end_et='2023-12-19T18:55:00+03:00',
            bbel_start_et='2023-12-20T04:56:00+03:00',
            sked_other='2023-12-19T05:00:00+03:00',
            at_other='2023-12-19T16:00:00+03:00',
            way_time=693,
            otpr='2023-12-19T18:55:00+03:00',
            prb=None,
            company=dict(
                name='Nordwind Airlines',
                code='N4',
                url_buy='https://nordwindairlines.ru/',
                url_register='https://airbook.nordwindairlines.ru/check-in/?lang=ru#search',
            )
        )
        self.assertDictEqual(FlightSchema(**valid_flight).model_dump(by_alias=True), valid_flight)