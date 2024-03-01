from typing import Annotated
from fastapi import APIRouter, Depends

from .queries.orm import SyncOrm
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
