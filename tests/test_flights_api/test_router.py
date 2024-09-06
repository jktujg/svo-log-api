from contextlib import nullcontext

import pytest
from sqlalchemy import select

from app.flights_api import models
from .payload import (
    aircraft,
    company,
    country,
    city,
    airport,
    flight,
    dt_string,
)
from ..utils import compare, get_recursive_value

# todo test company and airport with timerange and flight params


FOUND = nullcontext()
NOT_FOUND = pytest.raises(IndexError)


@pytest.mark.usefixtures('recreate_tables',)
class TestAircraft:
    async def test_upsert(self, session, client, random_superuser_headers):
        data = [aircraft(orig_id=1, name='first'), aircraft(orig_id=2, name='second')]
        update = [aircraft(orig_id=999, name='first')]
        country_query = select(models.AircraftModel).filter_by(name='first')

        response = client.put('/aircrafts', json=data, headers=random_superuser_headers)

        assert response.status_code == 200
        first_aircraft = (await session.execute(country_query)).scalar_one_or_none()
        assert first_aircraft.orig_id == 1
        session.expire(first_aircraft)

        update_response = client.put('/aircrafts', json=update, headers=random_superuser_headers)

        assert update_response.status_code == 200
        updated_first_aircraft = (await session.execute(country_query)).scalar_one_or_none()
        assert updated_first_aircraft.orig_id == 999

    @pytest.mark.parametrize(
        "data, params, expect",
        (
                (aircraft(name='first'), dict(), FOUND),

                (aircraft(name='first'), dict(name='irs'), FOUND),
                (aircraft(name='first'), dict(name='other'), NOT_FOUND),
        )
    )
    async def test_get_many_params(self, data, params, expect, client, random_superuser_headers):
        client.put('/aircrafts', json=[data], headers=random_superuser_headers)

        response = client.get('/aircrafts', params=params)
        content = response.json()

        assert response.status_code == 200
        with expect:
            assert compare(data, content['items'][0])

    async def test_get_many_by_name(self, session, client, random_superuser_headers):
        data = [aircraft(orig_id=1, name='first'), aircraft(orig_id=2, name='second')]
        client.put('/aircrafts', json=data, headers=random_superuser_headers)

        response = client.post('/aircrafts', json=['not_exists', 'first', 'first', 'not_exists', 'second'])
        content = response.json()

        assert response.status_code == 200
        assert content == [{}, data[0], data[0], {}, data[1]]


@pytest.mark.usefixtures('recreate_tables',)
class TestCountry:
    async def test_upsert(self, session, client, random_superuser_headers):
        data = [country(name='first', region='region'), country(name='second', region=None)]
        update = [country(name='first', region='new region')]
        country_query = select(models.CountryModel).filter_by(name='first')

        response = client.put('/countries', json=data, headers=random_superuser_headers)

        assert response.status_code == 200
        first_country = (await session.execute(country_query)).scalar_one_or_none()
        assert first_country.region == 'region'
        session.expire(first_country)

        update_response = client.put('/countries', json=update, headers=random_superuser_headers)

        assert update_response.status_code == 200
        updated_first_country = (await session.execute(country_query)).scalar_one_or_none()
        assert updated_first_country.region == 'new region'

    @pytest.mark.parametrize(
        "data, params, expect",
        (
                (country(region='first'), dict(), FOUND),

                (country(region='first'), dict(region='fir'), FOUND),
                (country(region='first'), dict(region='other'), NOT_FOUND),
        )
    )
    async def test_get_many_params(self, data, params, expect, client, random_superuser_headers):
        client.put('/countries', json=[data], headers=random_superuser_headers)

        response = client.get('/countries', params=params)
        content = response.json()

        assert response.status_code == 200
        with expect:
            assert content['items'][0] == data

    async def test_get_many_by_name(self, session, client, random_superuser_headers):
        data = [country(name='first', region='region'), country(name='second', region='other')]
        client.put('/countries', json=data, headers=random_superuser_headers)

        response = client.post('/countries', json=['not_exists', 'first', 'first', 'not_exists', 'second'])
        content = response.json()

        assert response.status_code == 200
        assert content == [{}, data[0], data[0], {}, data[1]]


@pytest.mark.usefixtures('recreate_tables',)
class TestCompany:
    async def test_upsert(self, session, client, random_superuser_headers):
        data = [company(iata='SU', name='first'), company(iata='N4', name='second')]
        update = [company(iata='SU', name='new')]
        company_query = select(models.CompanyModel).filter_by(iata='SU')

        response = client.put('/companies', json=data, headers=random_superuser_headers)

        assert response.status_code == 200
        first_company = (await session.execute(company_query)).scalar_one_or_none()
        assert first_company.name == 'first'
        session.expire(first_company)

        update_response = client.put('/companies', json=update, headers=random_superuser_headers)

        assert update_response.status_code == 200
        updated_first_company = (await session.execute(company_query)).scalar_one_or_none()
        assert updated_first_company.name == 'new'

    @pytest.mark.parametrize(
        "data, params, expect",
        (
                (company(name='first'), dict(), FOUND),

                (company(name='first'), dict(name='irs'), FOUND),
                (company(name='first'), dict(name='other'), NOT_FOUND),
        )
    )
    async def test_get_many_params(self, data, params, expect, client, random_superuser_headers):

        client.put('/companies', json=[data], headers=random_superuser_headers)

        response = client.get('/companies', params=params)
        content = response.json()

        assert response.status_code == 200
        with expect:
            assert content['items'][0] == data

    async def test_get_many_by_name(self, session, client, random_superuser_headers):
        data = [company(iata='SU', name='first'), company(iata='N4', name='second')]
        client.put('/companies', json=data, headers=random_superuser_headers)

        response = client.post('/companies', json=['not_exists', 'SU', 'not_exists', 'N4', 'SU',])
        content = response.json()

        assert response.status_code == 200
        assert content == [{}, data[0], {}, data[1], data[0],]


@pytest.mark.usefixtures('recreate_tables',)
class TestCity:
    async def test_upsert(self, session, client, random_superuser_headers):
        data = [city(name='first', timezone='Europe', country=country(name='Russia')), city(name='second')]
        update = [city(name='first', timezone='Asia', country=country(name='Armenia'))]
        city_query = select(models.CityModel).filter_by(name='first')

        response = client.put('/cities', json=data, headers=random_superuser_headers)

        assert response.status_code == 200
        first_city = (await session.execute(city_query)).scalar_one_or_none()
        assert first_city.timezone == 'Europe'
        assert first_city.country_name == 'Russia'
        session.expire(first_city)

        update_response = client.put('/cities', json=update, headers=random_superuser_headers)

        assert update_response.status_code == 200
        update_first_city = (await session.execute(city_query)).scalar_one_or_none()
        assert update_first_city.timezone == 'Asia'
        assert update_first_city.country_name == 'Armenia'

    @pytest.mark.parametrize(
        "data, params, expect",
        (
                (city(name='first'), dict(), FOUND),

                (city(name='first'), dict(name='IRS'), FOUND),
                (city(name_ru='first'), dict(name='IRS'), FOUND),
                (city(name='first'), dict(name='other'), NOT_FOUND),

                (city(country=country(region='DOMESTIC')), dict(region='dom'), FOUND),
                (city(country=country(region='DOMESTIC')), dict(region='Asia'), NOT_FOUND),

                (city(country=country(name='Russia')), dict(country='russia'), FOUND),
                (city(country=country(name='Russia')), dict(country='China'), NOT_FOUND),

                (city(timezone='Europe/Moscow'), dict(timezone='Europe'), FOUND),
                (city(timezone='Europe/Moscow'), dict(timezone='Asia'), NOT_FOUND),
                # all params
                (
                        city(
                        name='Khabarovsk',
                        name_ru='Харабовск',
                        timezone='Asia/Vladivostok',
                        country=country(
                            name='Russia',
                            region='DOMESTIC'
                        )
                    ),
                        dict(
                        name='Харабовск',
                        timezone='Asia',
                        country='Russia',
                        region='domestic',
                    ),
                        FOUND
                )
        )
    )
    async def test_get_many_params(self, data, params, expect, client, random_superuser_headers):
        client.put('/cities', json=[data], headers=random_superuser_headers)

        response = client.get('/cities', params=params)
        content = response.json()

        assert response.status_code == 200
        with expect:
            assert content['items'][0] == data

    async def test_get_many_by_name(self, session, client, random_superuser_headers):
        data = [city(name='first', timezone='Europe'), city(name='second')]
        client.put('/cities', json=data, headers=random_superuser_headers)

        response = client.post('/cities', json=['not_exists_name', 'first', 'second', 'not_exists_name'])
        content = response.json()

        assert response.status_code == 200
        assert content == [{}, *data, {}]


@pytest.mark.usefixtures('recreate_tables',)
class TestAirport:
    async def test_upsert(self, session, client, random_superuser_headers):
        data = [airport(iata='ABA', name='first', city=city(name='old')), airport(iata='DME')]
        update = [airport(iata='ABA', name='Abakan', city=city(name='new'))]
        airport_query = select(models.AirportModel).filter_by(iata='ABA')

        response = client.put('/airports', json=data, headers=random_superuser_headers)

        assert response.status_code == 200
        first_airport = (await session.execute(airport_query)).scalar_one_or_none()
        assert first_airport.name == 'first'
        assert first_airport.city_name == 'old'
        session.expire(first_airport)

        update_response = client.put('/airports', json=update, headers=random_superuser_headers)

        assert update_response.status_code == 200
        updated_first_airport = (await session.execute(airport_query)).scalar_one_or_none()
        assert updated_first_airport.name == 'Abakan'
        assert updated_first_airport.city_name == 'new'

    @pytest.mark.parametrize(
        "data, params, expect",
        (
                (airport(name='Moscow'), dict(), FOUND),

                (airport(name='Moscow'), dict(name='cow'), FOUND),
                (airport(name_ru='Москва'), dict(name='москва'), FOUND),
                (airport(name='first'), dict(name='other'), NOT_FOUND),

                (airport(city=city(country=country(name='Armenia'))), dict(country='armen'), FOUND),
                (airport(city=city(country=country(name='Armenia'))), dict(country='Sweden'), NOT_FOUND),

                (airport(city=city(country=country(region='Europe'))), dict(region='EUROPE'), FOUND),
                (airport(city=city(country=country(region='Europe'))), dict(region='Asia'), NOT_FOUND),

                (airport(city=city(timezone='Europe/Moscow')), dict(timezone='Europe/'), FOUND),
                (airport(city=city(timezone='Europe/Moscow')), dict(timezone='Asia'), NOT_FOUND),

                (airport(city=city(name='Stockholm')), dict(city='holm'), FOUND),
                (airport(city=city(name_ru='Стокгольм')), dict(city='Стокгольм'), FOUND),
                (airport(city=city(name='Stockholm')), dict(city='Moscow'), NOT_FOUND),
                # all params
                (
                        airport(
                            name='Sheremetyevo',
                            city=city(
                                name='Moscow',
                                timezone='Europe/Moscow',
                                country=country(
                                    name='Russia',
                                    region='Europe',
                                )
                            )
                        ),
                        dict(
                            name='Sheremetyevo',
                            city='Moscow',
                            timezone='Europe',
                            country='Russia',
                            region='Europe',
                        ),
                        FOUND
                )

        )
    )
    async def test_get_many_params(self, data, params, expect, client, random_superuser_headers):
        client.put('/airports', json=[data], headers=random_superuser_headers)

        response = client.get('/airports', params=params)
        content = response.json()

        assert response.status_code == 200
        with expect:
            assert content['items'][0] == data

    async def test_get_many_by_iata(self, session, client, random_superuser_headers):
        data = [airport(iata='ABA', name='first'), airport(iata='DME', name='second')]
        client.put('/airports', json=data, headers=random_superuser_headers)

        response = client.post('/airports', json=['ABA', 'not_exists', 'DME', 'not_exists', 'ABA'])
        content = response.json()

        assert response.status_code == 200
        assert content == [data[0], {}, data[1], {}, data[0]]


@pytest.mark.usefixtures('recreate_tables',)
class TestFlight:
    async def test_upsert(self, session, client, random_superuser_headers):
        data = [flight(orig_id=1, company=company(iata='SU'), mar1=airport(iata='KHV')), flight(orig_id=2)]
        update = [flight(orig_id=1, company=company(iata='N4'), mar1=airport(iata='KGF'))]
        flight_query = select(models.FlightModel).filter_by(orig_id=1)

        response = client.put('/flights', json=data, headers=random_superuser_headers)

        assert response.status_code == 200
        first_flight = (await session.execute(flight_query)).scalar_one_or_none()
        assert first_flight.company_iata == 'SU'
        assert first_flight.mar1_iata == 'KHV'
        session.expire(first_flight)

        update_response = client.put('/flights', json=update, headers=random_superuser_headers)

        assert update_response.status_code == 200
        updated_first_flight = (await session.execute(flight_query)).scalar_one_or_none()
        assert updated_first_flight.company_iata == 'N4'
        assert updated_first_flight.mar1_iata == 'KGF'

    @pytest.mark.parametrize(
        "data, params, expect",
        (
                (flight(direction='arrival'), dict(), FOUND),
                (flight(direction='arrival'), dict(direction='arrival'), FOUND),
                (flight(direction='arrival'), dict(direction='departure'), NOT_FOUND),

                (flight(company=company(iata='SU')), dict(company='SU'), FOUND),
                (flight(company=company(iata='N4')), dict(company='SU,N4,5N'), FOUND),

                (flight(gate_id='B103'), dict(gate_id='B103'), FOUND),
                (flight(gate_id='B103'), dict(gate_id='103'), NOT_FOUND),

                (flight(mar1=airport(iata='SVO')), dict(destination='SVO'), FOUND),
                (flight(mar2=airport(iata='DME')), dict(destination='DME'), FOUND),
                (flight(mar2=airport(iata='KHV')), dict(destination='AER,KHV,EVN'), FOUND),

                (flight(term_local='B'), dict(term_local='B'), FOUND),

                (flight(number='1720'), dict(number='1720'), FOUND),
                # all params
                (
                        flight(
                            direction='arrival',
                            gate_id='C123',
                            mar1=airport(iata='SVO'),
                            mar2=airport(iata='KHV'),
                            term_local='C',
                            number='1720'),
                        dict(
                            direction='arrival',
                            gate_id='C123',
                            destination=('KHV'),
                            term_local='C',
                            number='1720'
                        ),
                        FOUND),
        )
    )
    async def test_get_many_params(self, data, params, expect, client, random_superuser_headers):
        client.put('/flights', json=[data], headers=random_superuser_headers)

        params.update(date_start=dt_string(days=-5), date_end=dt_string(days=1))
        response = client.get('/flights', params=params)
        content = response.json()

        assert response.status_code == 200
        with expect:
            assert compare(data, content['items'][0])

    @pytest.mark.parametrize(
        'params, expect_status, assert_msg',
        (
                (dict(date_start=dt_string(days=-3), date_end=dt_string(days=2)), 200, 'ok'),
                (dict(date_start=dt_string(days=-3)), 422, 'not passing required'),
                (dict(date_end=dt_string(days=-3)), 422, 'not passing required'),
                (dict(date_start=dt_string(days=-8), date_end=dt_string(days=0)), 400, 'required date params range exceeding'),
        )
    )
    async def test_get_many_required_params(self, params, expect_status, assert_msg, client):
        response = client.get('/flights', params=params)

        assert response.status_code == expect_status

    async def test_get_many_by_id(self, session, client, random_superuser_headers):
        data1 = flight()
        data2 = flight()
        client.put('/flights', json=[data1], headers=random_superuser_headers)
        client.put('/flights', json=[data2], headers=random_superuser_headers)

        response = client.post('/flights', json=[-100, 2, 1])
        content = response.json()

        assert response.status_code == 200
        assert compare({}, content[0])
        assert compare(data2, content[1])
        assert compare(data1, content[2])


@pytest.mark.parametrize(
    'endpoint',
    ('aircrafts', 'companies', 'countries', 'cities', 'airports', 'flights')
)
@pytest.mark.usefixtures('recreate_tables',)
class TestCommonNegative:
    async def test_upsert_invalid(self, endpoint, client, random_superuser_headers):
        data = {'not': 'valid'}
        response = client.put(endpoint, json=[data], headers=random_superuser_headers)

        assert response.status_code == 422
        assert response.json()['detail']

    async def test_upsert_basic_user_not_permitted(self, endpoint, client, random_user_headers):
        response_user = client.put(endpoint, json=[{}], headers=random_user_headers)

        assert response_user.status_code == 403
        assert response_user.json()['detail']

    async def test_upsert_not_auth_not_permitted(self, endpoint, client):
        response_user = client.put(endpoint, json=[{}])

        assert response_user.status_code == 401
        assert response_user.json()['detail']

    async def test_get_one_not_found(self, endpoint, session, client):
        response = client.get(f'/{endpoint}/123')
        content = response.json()

        assert response.status_code == 404
        assert content['detail'] == 'Not Found'


@pytest.mark.usefixtures('recreate_tables',)
class TestCommonPositive:
    @pytest.mark.parametrize(
        'endpoint, data, resource',
        [
            ['aircrafts', aircraft(name='su9'), 'su9'],
            ['companies', company(iata='SU'), 'SU'],
            ['countries', country(name='russia'), 'russia'],
            ['cities', city(name='moscow'), 'moscow'],
            ['airports', airport(iata='SVO'), 'SVO'],
            ['flights', flight(orig_id=1234), 1],
        ]
    )
    async def test_get_one(self, endpoint, data, resource, client, random_superuser_headers):
        client.put(endpoint, json=[data], headers=random_superuser_headers)

        response = client.get(f'/{endpoint}/{resource}')
        content = response.json()

        assert response.status_code == 200
        assert compare(data, content)

    @pytest.mark.parametrize(
        'endpoint, data, params',
        [
            ['aircrafts', [aircraft(name='first'), aircraft(name='last')], {}],
            ['companies', [company(iata='SU', name='first'), company(iata='5N', name='last')], {}],
            ['countries', [country(name='first'), country(name='last')], {}],
            ['cities', [city(name='first'), city(name='last')], {}],
            ['airports', [airport(iata='SVO', name='first'), airport(iata='DME', name='last')], {}],
            ['flights',
                [
                    flight(orig_id=1234, sked_local=dt_string(days=-2)),
                    flight(orig_id=5678, sked_local=dt_string(days=-1))
                ],
                     {'date_start': dt_string(days=-5),
                      'date_end': dt_string(days=1)}],
        ]
    )
    async def test_get_many(self, endpoint, data, session, params, client, random_superuser_headers):
        client.put(endpoint, json=data, headers=random_superuser_headers)

        response = client.get(endpoint, params=params)
        content = response.json()

        assert response.status_code == 200
        assert content['count'] == 2
        assert content['total'] == 2
        assert content['page'] == 0
        assert content['total_pages'] == 1
        assert len(content['items']) == 2
        assert compare(data[0], content['items'][0])        # default order is by name or orig_id
        assert compare(data[1], content['items'][1])

    @pytest.mark.parametrize(
        'endpoint, data_cb, order_by, params',
        (
                ('aircrafts', aircraft, 'name', dict()),

                ('companies', company, 'name', dict()),
                ('companies', company, 'name', dict(order_by='name')),
                ('companies', company, 'iata', dict(order_by='iata')),

                ('countries', country, 'name', dict()),

                ('cities', city, 'name', dict()),
                ('cities', city, 'name', dict(order_by='name')),
                ('cities', city, 'name_ru', dict(order_by='name_ru')),

                ('airports', airport, 'name', dict()),
                ('airports', airport, 'name', dict(order_by='name')),
                ('airports', airport, 'name_ru', dict(order_by='name_ru')),
                ('airports', airport, 'iata', dict(order_by='iata')),
                ('airports', airport, 'city.name', dict(order_by='city_name')),
                ('airports', airport, 'city.name_ru', dict(order_by='city_name_ru')),

                ('flights', flight, 'sked_local', dict(date_start=dt_string(days=-6), date_end=dt_string(days=1))),
                ('flights', flight, 'sked_local', dict(order_type='asc', date_start=dt_string(days=-6), date_end=dt_string(days=1))),
                ('flights', flight, 'sked_local', dict(order_type='desc', date_start=dt_string(days=-6), date_end=dt_string(days=1))),
        )
    )
    async def test_order(self, endpoint, data_cb, order_by, params, client, random_superuser_headers):
        data = [data_cb() for _ in range(30)]
        client.put(endpoint, json=data, headers=random_superuser_headers)

        response = client.get(endpoint, params=params)
        content = response.json()

        assert response.status_code == 200
        content_keys = [get_recursive_value(item, order_by) for item in content['items']]
        assert content_keys == sorted(content_keys, key=lambda key: key.lower(), reverse=params.get('order_type', 'asc') == 'desc')
