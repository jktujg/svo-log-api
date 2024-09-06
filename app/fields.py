from typing import Annotated
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import mapped_column
from functools import partial


created_at = Annotated[datetime, mapped_column(server_default=text("now()"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("now()"), onupdate=partial(datetime.now, timezone.utc))]
