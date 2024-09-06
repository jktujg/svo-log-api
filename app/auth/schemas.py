from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer

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

    @field_serializer('role', 'state', when_used='json')
    def stringify(self, field):
        return field.name


class UserInDB(User):
    hashed_password: str
