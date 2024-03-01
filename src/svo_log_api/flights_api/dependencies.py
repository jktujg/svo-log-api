from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from ..dependencies import get_session
from ..auth.dependencies import check_permission


connection = Annotated[Session, Depends(get_session)]
# todo replace integers with str for enum
upsert_permission = check_permission(role=3, state=2)
registered_permission = check_permission(role=1, state=2)
