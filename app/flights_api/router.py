from typing import Annotated, Literal, Union

from fastapi import APIRouter, Depends, Body

from . import errors
from . import services
from . import (
    schemas,
    dependencies
)


airport_router = APIRouter()


@airport_router.put('/aircrafts/', dependencies=[Depends(dependencies.upsert_permission)], tags=['Aircrafts'])
async def upsert_aircrafts(
        session: dependencies.async_session,
        aircrafts: list[schemas.AircraftDBSchema]
):
    await services.AircraftService.upsert_many(session, aircrafts)


@airport_router.get('/aircrafts/', response_model=schemas.AircraftPagedResponseSchema, tags=['Aircrafts'])
async def get_aircrafts(
        session: dependencies.async_session,
        paging: Annotated[schemas.PagingSchema, Depends()],
        params: Annotated[schemas.AircraftQuerySchema, Depends()],
):
    return await services.AircraftService.get_many(
        session,
        paging=paging,
        order_by='name',
        **params.model_dump(by_alias=True, exclude_none=True)
    )


@airport_router.post('/aircrafts/', response_model=list[Union[schemas.AircraftResponseSchema, schemas.EmptySchema]], tags=['Aircrafts'])
async def get_aircrafts_by_id(
        session: dependencies.async_session,
        ids: Annotated[list[str], Body(max_length=100)],
):
    return await services.AircraftService.get_many_by_ids(session, ids=ids)


@airport_router.get('/aircrafts/{name}', response_model=schemas.AircraftResponseSchema, tags=['Aircrafts'])
async def get_aircraft(
        session: dependencies.async_session,
        name: str
):
    aircraft = await services.AircraftService.get_one(session=session, id=name)
    if aircraft is None:
        raise errors.NOT_FOUND
    else:
        return aircraft


@airport_router.put('/countries/', dependencies=[Depends(dependencies.upsert_permission)], tags=['Countries'])
async def upsert_countries(
        session: dependencies.async_session,
        countries: list[schemas.CountryDBSchema]
):
    await services.CountryService.upsert_many(session=session, data=countries)


@airport_router.get('/countries/', response_model=schemas.CountryPagedResponseSchema, tags=['Countries'])
async def get_countries(
        session: dependencies.async_session,
        paging: Annotated[schemas.PagingSchema, Depends()],
        params: Annotated[schemas.CountryQuerySchema, Depends()]):

    return await services.CountryService.get_many(
        session,
        paging=paging,
        **params.model_dump(by_alias=True, exclude_none=True)
    )


@airport_router.post('/countries/', response_model=list[Union[schemas.CountryResponseSchema, schemas.EmptySchema]], tags=['Countries'])
async def get_countries_by_id(
        session: dependencies.async_session,
        ids: Annotated[list[str], Body(max_length=100)],
):
    return await services.CountryService.get_many_by_ids(session, ids=ids)


@airport_router.get('/countries/{name}', response_model=schemas.CountryResponseSchema, tags=['Countries'])
async def get_country(
        session: dependencies.async_session,
        name: str
):
    country = await services.CountryService.get_one(session=session, id=name)
    if country is None:
        raise errors.NOT_FOUND
    else:
        return country


@airport_router.put('/cities/', dependencies=[Depends(dependencies.upsert_permission)], tags=['Cities'])
async def upsert_cities(
        session: dependencies.async_session,
        cities: list[schemas.CityDBSchema]
):
    await services.CityService.upsert_many(session=session, data=cities)


@airport_router.get('/cities/', response_model=schemas.CityPagedResponseSchema, tags=['Cities'])
async def get_cities(
        session: dependencies.async_session,
        paging: Annotated[schemas.PagingSchema, Depends()],
        params: Annotated[schemas.CityQuerySchema, Depends()],
        order_by: Literal['name', 'name_ru'] = 'name',
):
    return await services.CityService.get_many(
        session,
        paging=paging,
        order_by=order_by,
        **params.model_dump(by_alias=True, exclude_none=True)
    )


@airport_router.post('/cities/', response_model=list[Union[schemas.CityResponseSchema, schemas.EmptySchema]], tags=['Cities'])
async def get_cities_by_id(
        session: dependencies.async_session,
        ids: Annotated[list[str], Body(max_length=100)],
):
    return await services.CityService.get_many_by_ids(session, ids=ids)


@airport_router.get('/cities/{name}', response_model=schemas.CityResponseSchema, tags=['Cities'])
async def get_city(
        session: dependencies.async_session,
        name: str
):
    city = await services.CityService.get_one(session=session, id=name)
    if city is None:
        raise errors.NOT_FOUND
    else:
        return city


@airport_router.put('/airports/', dependencies=[Depends(dependencies.upsert_permission)], tags=['Airports'])
async def upsert_airports(
        session: dependencies.async_session,
        airports: list[schemas.AirportDBSchema]
):
    await services.AirportService.upsert_many(session, airports)


@airport_router.get('/airports/', response_model=schemas.AirportPagedResponseSchema, tags=['Airports'])
async def get_airports(
        session: dependencies.async_session,
        paging: Annotated[schemas.PagingSchema, Depends()],
        params: Annotated[schemas.AirportQuerySchema, Depends()],
        order_by: Literal['name', 'name_ru', 'iata', 'city_name', 'city_name_ru'] = 'name',
):
    return await services.AirportService.get_many(
        session,
        paging=paging,
        order_by=order_by,
        **params.model_dump(by_alias=True, exclude_none=True)
    )


@airport_router.post('/airports/', response_model=list[Union[schemas.AirportResponseSchema, schemas.EmptySchema]], tags=['Airports'])
async def get_airports_by_id(
        session: dependencies.async_session,
        ids: Annotated[list[str], Body(max_length=100)],
):
    return await services.AirportService.get_many_by_ids(session, ids=ids)


@airport_router.get('/airports/{iata}', response_model=schemas.AirportResponseSchema, tags=['Airports'])
async def get_airport(
        session: dependencies.async_session,
        iata: str
):
    airport = await services.AirportService.get_one(session=session, id=iata.upper())
    if airport is None:
        raise errors.NOT_FOUND
    else:
        return airport


@airport_router.put('/companies/', dependencies=[Depends(dependencies.upsert_permission)], tags=['Companies'])
async def upsert_companies(
        session: dependencies.async_session,
        companies: list[schemas.CompanyDBSchema]
):
    await services.CompanyService.upsert_many(session, companies)


@airport_router.get('/companies/', response_model=schemas.CompanyPagedResponseSchema, tags=['Companies'])
async def get_companies(
        session: dependencies.async_session,
        paging: Annotated[schemas.PagingSchema, Depends()],
        params: Annotated[schemas.CompanyQuerySchema, Depends()],
        order_by: Literal['name', 'iata'] = 'name',
):
    return await services.CompanyService.get_many(
        session,
        paging=paging,
        order_by=order_by,
        **params.model_dump(by_alias=True, exclude_none=True)
    )


@airport_router.post('/companies/', response_model=list[Union[schemas.CompanyResponseSchema, schemas.EmptySchema]], tags=['Companies'])
async def get_companies_by_id(
        session: dependencies.async_session,
        ids: Annotated[list[str], Body(max_length=100)],
):
    return await services.CompanyService.get_many_by_ids(session, ids=ids)


@airport_router.get('/companies/{iata}', response_model=schemas.CompanyResponseSchema, tags=['Companies'])
async def get_company(
        session: dependencies.async_session,
        iata: str
):
    company = await services.CompanyService.get_one(session=session, id=iata.upper())
    if company is None:
        raise errors.NOT_FOUND
    else:
        return company


@airport_router.put('/flights/', dependencies=[Depends(dependencies.upsert_permission)], tags=['Flights'])
async def upsert_flights(
        session: dependencies.async_session,
        flights: list[schemas.FlightDBSchema]
):
    await services.FlightService.upsert_many(session, flights)


@airport_router.get('/flights/', response_model=schemas.FlightPagedResponseSchema, tags=['Flights'])
async def get_flights(
        session: dependencies.async_session,
        paging: Annotated[schemas.PagingSchema, Depends()],
        params: Annotated[schemas.FlightQuerySchema, Depends()],
        order_type: Literal['asc', 'desc'] = 'asc',
):
    return await services.FlightService.get_many(
        session,
        paging=paging,
        **params.model_dump(by_alias=True, exclude_none=True),
        order_by='sked_local',
        order_type=order_type,
    )


@airport_router.post('/flights/', response_model=list[Union[schemas.FlightResponseSchema, schemas.EmptySchema]], tags=['Flights'])
async def get_flights_by_id(
        session: dependencies.async_session,
        ids: Annotated[list[int], Body(max_length=100)],
):
    return await services.FlightService.get_many_by_ids(session, ids=ids)


@airport_router.get('/flights/{id}', response_model=schemas.FlightResponseSchema, tags=['Flights'])
async def get_flight(
        session: dependencies.async_session,
        id: int,
        changelog: bool = True,
):
    join_relations = ('changelog',) if changelog else None
    flight = await services.FlightService.get_one(session=session, id=id, join_relations=join_relations)
    if flight is None:
        raise errors.NOT_FOUND
    else:
        return flight
