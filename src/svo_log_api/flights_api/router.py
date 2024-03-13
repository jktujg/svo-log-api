import math
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from .queries.orm import SyncOrm
from . import utils
from . import (
    schemas,
    dependencies
)

airport_router = APIRouter()


@airport_router.put('/aircrafts/', dependencies=[Depends(dependencies.upsert_permission)])
def upsert_aircrafts(conn: dependencies.connection, aircrafts: list[schemas.AircraftSchema]):
    SyncOrm.upsert_aircrafts(conn, aircrafts)


@airport_router.put('/countries/', dependencies=[Depends(dependencies.upsert_permission)])
def upsert_countries(conn: dependencies.connection, countries: list[schemas.CountrySchema]):
    SyncOrm.upsert_countries(conn, countries)


@airport_router.put('/cities/', dependencies=[Depends(dependencies.upsert_permission)])
def upsert_cities(conn: dependencies.connection, cities: list[schemas.CitySchema]):
    SyncOrm.upsert_cities(conn, cities)


@airport_router.put('/airports/', dependencies=[Depends(dependencies.upsert_permission)])
def upsert_airports(conn: dependencies.connection, airports: list[schemas.AirportSchema]):
    SyncOrm.upsert_airports(conn, airports)


@airport_router.put('/companies/', dependencies=[Depends(dependencies.upsert_permission)])
def upsert_companies(conn: dependencies.connection, companies: list[schemas.CompanySchema]):
    SyncOrm.upsert_companies(conn, companies)


@airport_router.put('/flights/', dependencies=[Depends(dependencies.upsert_permission)])
def upsert_flights(conn: dependencies.connection, flights: list[schemas.FlightSchema]):
    SyncOrm.upsert_flights(conn, flights)


@airport_router.get('/flights/', response_model=schemas.FlightResponseContainer)
def get_flights(
        conn: dependencies.connection,
        params: Annotated[schemas.FlightsGetParamsSchema, Depends()],
        paging: Annotated[schemas.PagingSchema, Depends()],
        changelog: bool = False,
):
    flight_ids = SyncOrm.get_flight_ids(conn, params=params)                  # caching
    paged_ids = utils.get_page(flight_ids, page=paging.page, limit=paging.limit)
    flights = SyncOrm.get_flights_by_ids(conn, ids=paged_ids, changelog=changelog)
    #todo добавить отдельную схему под пагинацию (Pagination)
    return dict(
        flights=flights,
        count=len(flights),
        total=len(flight_ids),
        page=paging.page,
        total_pages=math.ceil(len(flight_ids) / paging.limit),
    )


@airport_router.get('/flights/{flight_id}', response_model=schemas.FlightResponseSchema)
def get_flight(conn: dependencies.connection, flight_id: int, changelog: bool = False):
    flight = SyncOrm.get_flights_by_ids(conn, ids=[flight_id], changelog=changelog)

    if not flight:
        raise HTTPException(status_code=404, detail='Not Found')
    return flight[0]
