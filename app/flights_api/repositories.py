import operator
from collections import namedtuple
from functools import cached_property
from typing import Sequence, Iterable, Any, Literal, Type, TypeVar

import regex
from sqlalchemy import select, inspect, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, noload

from . import (
    models,
    patterns,
    utils,
)


Change = namedtuple('Change', field_names=['model', 'old_val', 'field'])


class Repository():
    model = TypeVar('model', bound=Type[models.Base])
    unique_key: str
    order_key_map: dict = {}

    async def upsert_many(self, session: AsyncSession, data: Iterable[dict]) -> Sequence[Change]:
        _data = {record[self.unique_key]: record for record in data}
        changelog = []

        exists_query = (
            select(self.model)
            .filter(getattr(self.model, self.unique_key).in_(list(_data.keys())))
        )
        existed_models = (await session.execute(exists_query)).scalars().all()

        for model in existed_models:
            record = _data[getattr(model, self.unique_key)]
            for col_name in self._update_columns:
                if (old_val := getattr(model, col_name)) != (new_val := record[col_name]):
                    setattr(model, col_name, new_val)
                    changelog.append(Change(model=model, old_val=old_val, field=col_name))
            _data.pop(getattr(model, self.unique_key))

        new_models = [self.model(**record) for record in _data.values()]
        session.add_all(new_models)

        await self._update_changelog(session, changelog)
        return changelog

    async def get_many_ids(self,
                           session: AsyncSession,
                           order_by: str | None = None,
                           order_type: Literal['asc', 'desc'] = 'asc',
                           **params
                           ) -> Sequence:

        order_by = self._order_parse(order_by)
        query = select(self._model_pk, order_by).distinct().order_by(getattr(order_by, order_type)())
        query, joins = self._add_filters(query, params)

        if order_by.parent.class_ is not self.model and order_by.parent.class_ not in joins:
            query = query.join(order_by.parent.class_)

        resp = await session.execute(query)
        ids = resp.scalars().all()

        return ids

    async def get_many(self,
                       session: AsyncSession,
                       ids,
                       include: set | None = None,
                       exclude: set | None = None,
                       order_by: Any | None = None,
                       order_type: Literal['asc', 'desc'] = 'asc',
                       **kw
                       ) -> Sequence[model]:

        if (include and exclude) and (exclude & include):
            raise Exception('Intersection of include and exclude')

        order_by = self._order_parse(order_by)
        query = (
            select(self.model)
            .order_by(getattr(order_by, order_type)())
            .options(*(joinedload(getattr(self.model, field)) for field in include or []))
            .options(*(noload(getattr(self.model, field)) for field in exclude or []))
            .filter(self._model_pk.in_(ids))
        )

        if order_by.parent.class_ is not self.model:
            query = query.join(order_by.parent.class_)

        models = (await session.execute(query)).scalars().all()
        return models

    async def get_one(self, session: AsyncSession, id: str, join_relations: tuple | None = None) -> model | None:
        query = (
            select(self.model)
            .filter(self._model_pk == id)
            .options(*(joinedload(getattr(self.model, rel_field)) for rel_field in join_relations or []))
        )

        model = (await session.execute(query)).unique().scalar_one_or_none()
        return model

    @cached_property
    def _model_pk(self):
        return getattr(self.model, inspect(self.model).primary_key[0].name)

    @cached_property
    def _update_columns(self) -> tuple[str]:
        return utils.get_columns(self.model, exclude={'created_at', 'updated_at'})

    async def _update_changelog(self, session: AsyncSession, changelog: Sequence[Change]) -> None:
        ...

    def _order_parse(self, order: str | None):
        return (
                self.order_key_map.get(order)
                or getattr(self.model, order, None) if order is not None else None
                or self._model_pk
        )

    def _add_filters(self, query, params: dict):
        filters = []
        joins = {}
        match = {}

        for key, val in params.items():
            if val is None:
                continue

            match = regex.fullmatch(patterns.relation_alias, key).capturesdict()

            relations = [getattr(models, rel) for rel in match['relations']]
            relation_model = relations[-1] if relations else self.model

            sub_filters = []
            for field in match['fields']:
                if match['meth']:
                    sub_filters.append(getattr(getattr(relation_model, field), match['meth'][0])(val))
                elif match['op']:
                    sub_filters.append(getattr(operator, match['op'][0])(getattr(relation_model, field), val))
                else:
                    sub_filters.append(getattr(relation_model, field) == val)

            for rel in relations:
                joins[rel] = None

            filters.append(or_(*sub_filters))

        for e, j in enumerate(joins):
            if e == len(joins) - 1 and (clauses := match.get('clauses')):
                query = query.join(j, or_(self._model_pk == getattr(j, clause) for clause in clauses))
            else:
                query = query.join(j)
        query = query.filter(and_(True, *filters))

        return query, joins


class AircraftRepository(Repository):
    model = models.AircraftModel
    unique_key = 'name'


class CountryRepository(Repository):
    model = models.CountryModel
    unique_key = 'name'


class CityRepository(Repository):
    model = models.CityModel
    unique_key = 'name'


class AirportRepository(Repository):
    model = models.AirportModel
    unique_key = 'iata'
    order_key_map = dict(
        city_name=models.CityModel.name,
        city_name_ru=models.CityModel.name_ru,
    )


class CompanyRepository(Repository):
    model = models.CompanyModel
    unique_key = 'iata'


class FlightRepository(Repository):
    model = models.FlightModel
    changelog_model = models.FlightsChangelogModel
    unique_key = 'orig_id'

    async def _update_changelog(self, session: AsyncSession, changelog: Sequence[Change]) -> None:
        flights_changelog = [self.changelog_model(field=c.field, old_value=c.old_val, flight=c.model)
                             for c in changelog]
        session.add_all(flights_changelog)
