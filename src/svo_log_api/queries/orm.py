from typing import Sequence, Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from collections import defaultdict

from .. import models
from .. import schemas
from .. import utils


class SyncOrm:

    @staticmethod
    def upsert_aircrafts(conn: Session, data: Iterable[BaseModel]) -> Sequence[models.AircraftModel]:
        unique_aircrafts = utils.unique_schemas(data, unique_keys=['orig_id'])

        stmt = (
            insert(models.AircraftModel)
            .returning(models.AircraftModel)
            .values([a.model_dump() for a in unique_aircrafts])
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[models.AircraftModel.__table__.columns.orig_id],
            set_=dict(name=stmt.excluded.name)
        )

        res = conn.execute(stmt)
        conn.commit()

        return res.scalars().all()

    @staticmethod
    def upsert_countries(conn: Session, data: Iterable[BaseModel]) -> Sequence[models.CountryModel]:
        unique_countries = utils.unique_schemas(data, unique_keys=['name'])

        stmt = (
            insert(models.CountryModel)
            .returning(models.CountryModel)
            .values([c.model_dump() for c in unique_countries])
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[models.CountryModel.__table__.columns.name],
            set_=dict(region=stmt.excluded.region),
        )

        res = conn.execute(stmt)
        conn.commit()

        return res.scalars().all()

    @staticmethod
    def upsert_airports(conn: Session, data: Iterable[schemas.AirportSchema]) -> Sequence[models.AirportModel]:
        unique_airports = utils.unique_schemas(data, unique_keys=['orig_id', 'iata', 'icao'])

        countries = [a.country for a in unique_airports if a.country is not None]
        if countries:
            SyncOrm.upsert_countries(conn=conn, data=countries)

        stmt = (
            insert(models.AirportModel)
            .returning(models.AirportModel)
            .values([a.model_dump(exclude={'country'}) | {'country_id': select(models.CountryModel.id).where(models.CountryModel.name == a.country.name)} for a in unique_airports])
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[models.AirportModel.__table__.columns.iata],
            set_={column_name: getattr(stmt.excluded, column_name) for column_name in utils.get_columns(models.AirportModel).keys()}
        )

        res = conn.execute(stmt)
        conn.commit()

        return res.scalars().all()

    @staticmethod
    def upsert_companies(conn: Session, data: Iterable[schemas.CompanySchema]) -> Sequence[models.CompanyModel]:
        unique_companies = utils.unique_schemas(data, unique_keys=['iata'])

        stmt = (
            insert(models.CompanyModel)
            .returning(models.CompanyModel)
            .values([c.model_dump() for c in unique_companies])
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[models.CompanyModel.__table__.columns.iata],
            set_={column_name: getattr(stmt.excluded, column_name) for column_name in utils.get_columns(models.CompanyModel).keys()}
        )

        res = conn.execute(stmt)
        conn.commit()

        return res.scalars().all()

    @staticmethod
    def upsert_flights(conn: Session, data: Iterable[schemas.FlightSchema]) -> Sequence[models.FlightModel]:
        unique_flights = utils.unique_schemas(data, unique_keys=['orig_id'])

        relations = defaultdict(list)
        for flight in unique_flights:
            relations['companies'].append(flight.company)
            relations['aircrafts'].append(flight.aircraft)
            for i in range(1, 6):
                relations['airports'].append(getattr(flight, f'mar{i}'))

        not_none = lambda x: x is not None
        companies = {c.iata: c for c in SyncOrm.upsert_companies(conn, filter(not_none, relations['companies']))}
        aircrafts = {a.orig_id: a for a in SyncOrm.upsert_aircrafts(conn, filter(not_none, relations['aircrafts']))}
        airports = {a.iata: a for a in SyncOrm.upsert_airports(conn, filter(not_none, relations['airports']))}

        stmt = (
            insert(models.FlightModel)
            .returning(models.FlightModel)
            .values([(
                f.model_dump(exclude={'company', 'aircraft', *[f'mar{i}' for i in range(1, 6)]})
                | dict(company_id=companies[f.company.iata].id,
                       aircraft_id=aircrafts[f.aircraft.orig_id].id,
                       mar1_id=airports[f.mar1.iata].id if f.mar1 else None,
                       mar2_id=airports[f.mar2.iata].id if f.mar2 else None,
                       mar3_id=airports[f.mar3.iata].id if f.mar3 else None,
                       mar4_id=airports[f.mar4.iata].id if f.mar4 else None,
                       mar5_id=airports[f.mar5.iata].id if f.mar5 else None,
                       )
            ) for f in unique_flights])
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[models.FlightModel.__table__.columns.orig_id],
            set_={column_name: getattr(stmt.excluded, column_name) for column_name in utils.get_columns(models.FlightModel).keys()}
        )

        res = conn.execute(stmt)
        conn.commit()

        return res.scalars().all()
