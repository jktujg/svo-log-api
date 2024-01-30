from typing import Sequence

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel

from .. import models
from .. import schemas
from .. import utils


class SyncOrm:

    @staticmethod
    def upsert_aircrafts(conn: Session, data: Sequence[BaseModel]) -> Sequence[models.AircraftModel]:
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
    def upsert_countries(conn: Session, data: Sequence[BaseModel]) -> Sequence[models.CountryModel]:
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
    def upsert_airports(conn: Session, data: Sequence[schemas.AirportSchema]) -> Sequence[models.AirportModel]:
        unique_airports = utils.unique_schemas(data, unique_keys=['orig_id', 'iata', 'icao'])

        countries = [a.country for a in unique_airports if a is not None]
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

    def upsert_companies(self, data: list):
        ...

    def upsert_flights(self, data: list):
        ...
