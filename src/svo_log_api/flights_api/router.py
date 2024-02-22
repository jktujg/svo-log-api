from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas
from .queries.orm import SyncOrm
from ..dependencies import get_session
from ..auth.dependencies import check_permission

airport_router = APIRouter()
connection = Annotated[Session, Depends(get_session)]
upsert_permission = Depends(check_permission(role=3, state=2))


@airport_router.put('/aircrafts/', dependencies=[upsert_permission])
def upsert_aircrafts(conn: connection, aircrafts: list[schemas.AircraftSchema]):
    SyncOrm.upsert_aircrafts(conn, aircrafts)


@airport_router.put('/countries/', dependencies=[upsert_permission])
def upsert_countries(conn: connection, countries: list[schemas.CountrySchema]):
    SyncOrm.upsert_countries(conn, countries)


@airport_router.put('/cities/', dependencies=[upsert_permission])
def upsert_cities(conn: connection, cities: list[schemas.CitySchema]):
    SyncOrm.upsert_cities(conn, cities)


@airport_router.put('/airports/', dependencies=[upsert_permission])
def upsert_airports(conn: connection, airports: list[schemas.AirportSchema]):
    SyncOrm.upsert_airports(conn, airports)


@airport_router.put('/companies/', dependencies=[upsert_permission])
def upsert_companies(conn: connection, companies: list[schemas.CompanySchema]):
    SyncOrm.upsert_companies(conn, companies)


@airport_router.put('/flights/', dependencies=[upsert_permission])
def upsert_flights(conn: connection, flights: list[schemas.FlightSchema]):
    SyncOrm.upsert_flights(conn, flights)
