from typing import Annotated

from fastapi import HTTPException, Form
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.auth import models, errors, security, schemas
from app.auth.dependencies import async_session
from app.auth.models import UserModel
from app.auth.permissions import UserRole, UserState
from app.auth.crud import AsyncOrm
from app.auth.utils import password_is_valid


async def register_user(session, email: str, password: str, role: UserRole, state: UserState) -> models.UserModel:
    if password_is_valid(password) == False:
        raise errors.PASSWORD_STRENGTH_ERROR
    hashed_password = security.get_password_hash(password)
    try:
        new_user = schemas.UserInDB(
            email=email,
            hashed_password=hashed_password,
            role=role,
            state=state,
        )
    except ValidationError as err:
        raise HTTPException(status_code=401, detail=str({e['loc'][0]: e['msg'] for e in err.errors()}))

    try:
        registered_user = await AsyncOrm.create_user(session, new_user)
    except IntegrityError:
        raise errors.REGISTER_LOGIN_ERROR

    return registered_user


async def register_basic_user(session: async_session, username: Annotated[str, Form()], password: Annotated[str, Form()]) -> UserModel | None:
    user = await register_user(session, username, password, role=UserRole.USER, state=UserState.ACTIVE)
    return user
