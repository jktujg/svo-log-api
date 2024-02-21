from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from .permissions import UserRole, UserState


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    email: EmailStr
    role: UserRole
    state: UserState
    exp: datetime | None = None


class User(BaseModel):
    email: EmailStr
    role: UserRole
    state: UserState


class UserInDB(User):
    hashed_password: str
