from typing import Annotated
from functools import wraps

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..queries.orm import SyncOrm
from ..database import session


airport_router = APIRouter()


def get_session(**params):
    def session_gen():
        with session(**params) as conn:
            yield conn
    return session_gen


@airport_router.put('/aircrafts/')
def upsert_aircrafts(conn: Annotated[Session, Depends(get_session(expire_on_commit=False))], aircrafts: list[schemas.AircraftSchema]):
    SyncOrm.upsert_aircarafts(conn, aircrafts)


@airport_router.put('/countries/')
def upsert_countries(conn: Annotated[Session, Depends(get_session(expire_on_commit=False))], countries: list[schemas.CountrySchema]):
    SyncOrm.upsert_countries(conn, countries)


@airport_router.put('/airports/')
def upsert_airports(conn: Annotated[Session, Depends(get_session(expire_on_commit=False))], airports: list[schemas.AirportSchema]):
    SyncOrm.upsert_airports(conn, airports)


@airport_router.put('/companies/')
def upsert_companies(conn: Annotated[Session, Depends(get_session(expire_on_commit=False))], companies: list[schemas.CompanySchema]):
    SyncOrm.upsert_companies(conn, companies)


@airport_router.put('/flights/')
def upsert_flights(conn: Annotated[Session, Depends(get_session(expire_on_commit=False))], flights: list[schemas.FlightSchema]):
    SyncOrm.upsert_flights(conn, flights)
