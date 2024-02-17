from pydantic import BaseModel
from typing import Iterable, Optional
from collections import defaultdict
from sqlalchemy.orm import DeclarativeBase


def unique_schemas(schemas: Iterable[BaseModel], unique_keys: Iterable) -> list[BaseModel]:
    hash_map = defaultdict(set)
    result = []

    for s in schemas:
        for k in unique_keys:
            if getattr(s, k) in hash_map[k]:
                break
        else:
            for k in unique_keys:
                hash_map[k].add(getattr(s, k))
            result.append(s)

    return result


def get_columns(model: DeclarativeBase, exclude: Optional[Iterable] = tuple(), include_primary: bool = False):
    """ """
    columns = dict(model.__table__.columns.items())

    for column_name in exclude:
        columns.pop(column_name, None)

    if not include_primary:
        for name in list(columns):
            if columns[name].primary_key:
                columns.pop(name)

    return columns

