from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_async_session
from ..auth.dependencies import check_permission
from ..auth.permissions import UserRole, UserState


async_session = Annotated[AsyncSession, Depends(get_async_session)]
upsert_permission = check_permission(role=UserRole.ADMIN, state=UserState.ACTIVE)
registered_permission = check_permission(role=UserRole.USER, state=UserState.ACTIVE)
