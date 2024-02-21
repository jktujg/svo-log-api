from datetime import timedelta, datetime
from typing import Annotated, Callable
from pydantic import ValidationError

from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from . import (
    errors,
    schemas,
    encryption
)
from .queries import SyncOrm
from .models import UserModel
from .config import auth_settings
from .permissions import UserState, UserRole
from ..dependencies import get_session
from ..config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.ROOT_PATH + settings.AUTH_PATH + '/token')


def authenticate_user(
        conn: Annotated[Session, Depends(get_session(expire_on_commit=False))],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> UserModel | None:

    user = SyncOrm.get_user(conn=conn, email=form_data.username)
    if not (user or encryption.verify_password(form_data.password, user.hashed_password)):
        raise errors.login_error
    else:
        return user


def create_access_token(user: UserModel, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    payload = schemas.TokenData.model_validate(user, from_attributes=True)
    payload.exp = expire

    encoded_jwt = jwt.encode(payload.model_dump(), auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt


def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        token_data = schemas.TokenData(**payload)
    except JWTError:
        raise errors.credential_exception

    return token_data


def get_current_user(
        conn: Annotated[Session, Depends(get_session(expire_on_commit=False))],
        token_data: Annotated[schemas.TokenData, Depends(get_token_data)]
) -> UserModel | None:

    user = SyncOrm.get_user(conn=conn, email=token_data.email)
    if user is None:
        raise errors.credential_exception
    return user


def register_user(conn: Annotated[Session, Depends(get_session(expire_on_commit=False))], username: Annotated[str, Form()], password: Annotated[str, Form()]) -> UserModel | None:
    hashed_password = encryption.get_password_hash(password)
    try:
        new_user = schemas.UserInDB(
            email=username,
            hashed_password=hashed_password,
            role=UserRole.USER,
            state=UserState.INACTIVE,
        )
    except ValidationError as err:
        raise HTTPException(status_code=401, detail=str({e['loc'][0]: e['msg'] for e in err.errors()}))

    registered_user = SyncOrm.create_user(conn, new_user)
    if not registered_user:
        raise errors.register_login_error

    return registered_user


def check_permission(role: UserRole | int, state: UserState | int) -> Callable:

    def is_permitted(token_data: Annotated[schemas.TokenData, Depends(get_token_data)]) -> bool:
        if token_data.role >= role and token_data.state >= state:
            return True
        else:
            raise errors.permission_error

    return is_permitted





