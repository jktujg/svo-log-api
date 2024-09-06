from typing import Annotated, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from . import (
    errors,
    schemas,
    security
)
from .config import auth_settings
from ..config import settings
from .models import UserModel
from .permissions import UserState, UserRole
from .crud import AsyncOrm
from ..dependencies import get_async_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.ROOT_PATH + settings.AUTH_PATH + '/token')
async_session = Annotated[AsyncSession, Depends(get_async_session)]


async def authenticate_user(
        session: async_session,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> UserModel | None:

    user = await AsyncOrm.get_user(session=session, email=form_data.username)
    if not (user and security.verify_password(form_data.password, user.hashed_password)):
        raise errors.LOGIN_ERROR
    else:
        return user


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenData(**payload)
    except JWTError:
        raise errors.CREDENTIAL_EXCEPTION

    return token_data


async def get_current_user(
        session: async_session,
        token_data: Annotated[schemas.TokenData, Depends(get_token_data)]
) -> UserModel | None:

    user = await AsyncOrm.get_user(session=session, email=token_data.email)
    if user is None:
        raise errors.CREDENTIAL_EXCEPTION
    return user


def check_permission(role: UserRole | int, state: UserState | int) -> Callable:

    async def is_permitted(token_data: Annotated[schemas.TokenData, Depends(get_token_data)]) -> bool:
        if token_data.role >= role and token_data.state >= state:
            return True
        else:
            raise errors.PERMISSION_ERROR

    return is_permitted
