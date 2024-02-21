from typing import Annotated
from fastapi import APIRouter, Depends

from . import (
    dependencies,
    schemas,
    models,
)


auth_router = APIRouter()


@auth_router.post('/token', response_model=schemas.Token)
def login_for_access_token(user: Annotated[models.UserModel, Depends(dependencies.authenticate_user)]) -> dict:
    access_token = dependencies.create_access_token(user)
    return dict(access_token=access_token, token_type='bearer')


@auth_router.get('/users/me', response_model=schemas.User)
def read_users_me(current_user: Annotated[models.UserModel, Depends(dependencies.get_current_user)]):
    return current_user
