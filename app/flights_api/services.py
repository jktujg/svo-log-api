import math
from typing import Any, Collection, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from . import (
    repositories,
    schemas,
)


class Service:
    repo = TypeVar('repo', bound=repositories.Repository)

    @classmethod
    async def upsert_many(cls, session: AsyncSession, data: Collection[schemas.BaseSchema]) -> None:
        changelog = await cls.repo.upsert_many(session, [d.model_dump(by_alias=True) for d in data])

    @classmethod
    async def get_one(cls, session: AsyncSession, id: Any, join_relations: tuple | None = None):
        return await cls.repo.get_one(session, id=id, join_relations=join_relations)

    @classmethod
    async def get_many(cls, session: AsyncSession, paging: schemas.PagingSchema, **params) -> dict:
        ids = await cls.repo.get_many_ids(session, **params)
        paged_ids = paging.get_page(ids)
        models = await cls.repo.get_many(session, ids=paged_ids, **params)

        return dict(
            items=models,
            count=len(models),
            total=len(ids),
            page=paging.page,
            total_pages=math.ceil(len(ids) / paging.limit),
        )

    @classmethod
    async def get_many_by_ids(cls, session: AsyncSession, ids: list, **params) -> list:
        models = await cls.repo.get_many(session, ids=ids, **params)
        models_map = {getattr(m, cls.repo._model_pk.name): m for m in models}
        return [models_map.get(id, {}) for id in ids]


class AircraftService(Service):
    repo = repositories.AircraftRepository()


class CountryService(Service):
    repo = repositories.CountryRepository()


class CompanyService(Service):
    repo = repositories.CompanyRepository()


class CityService(Service):
    repo = repositories.CityRepository()

    @classmethod
    async def upsert_many(cls, session: AsyncSession, data: Collection[schemas.CityDBSchema]) -> None:
        await CountryService.upsert_many(session, [city.country for city in data])
        await cls.repo.upsert_many(session, [city.model_dump(by_alias=True) for city in data])


class AirportService(Service):
    repo = repositories.AirportRepository()

    @classmethod
    async def upsert_many(cls, session: AsyncSession, data: Collection[schemas.AirportDBSchema]) -> None:
        await CityService.upsert_many(session, [airport.city for airport in data])
        await cls.repo.upsert_many(session, [airport.model_dump(by_alias=True) for airport in data])


class FlightService(Service):
    repo = repositories.FlightRepository()

    @classmethod
    async def upsert_many(cls, session: AsyncSession, data: Collection[schemas.FlightDBSchema]) -> None:
        companies, aircrafts, airports = set(), set(), set()
        for flight in data:
            companies.add(flight.company)
            aircrafts.add(flight.aircraft)
            for n in range(1, 6):
                if (airport := getattr(flight, f'mar{n}')) is not None:
                    airports.add(airport)

        await AircraftService.upsert_many(session, aircrafts)
        await CompanyService.upsert_many(session, companies)
        await AirportService.upsert_many(session, airports)

        await cls.repo.upsert_many(session, [flight.model_dump(by_alias=True) for flight in data])
