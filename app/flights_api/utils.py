from datetime import timedelta
from typing import Iterable, Optional, Type

from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeBase


def get_columns(model: Type[DeclarativeBase], exclude: Optional[Iterable] = tuple(), include_primary: bool = False):
    columns = dict(model.__table__.columns.items())

    for column_name in exclude:
        columns.pop(column_name, None)

    if not include_primary:
        for pk_name in (c.name for c in model.__table__.primary_key):
            columns.pop(pk_name)

    return columns


def check_timedelta(self):
    """ Use as model_validator wrapped method for query schemas."""
    max_days = 7 #todo move to .env

    if self.date_end is not None or self.date_start is not None:
        try:
            delta = self.date_end - self.date_start
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect date_start or date_end format.\n'
                       'They must be both iso8601 format with timezone if any.'
            )
        else:
            if delta > timedelta(days=max_days):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Difference between start date and end date must be less then {max_days} days, current is {delta.days} days'
                )
