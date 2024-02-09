from enum import StrEnum
from typing import Annotated
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import mapped_column


created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]


class Direction(StrEnum):
    arrival = 'arrival'
    departure = 'departure'