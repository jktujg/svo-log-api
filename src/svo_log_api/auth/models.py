from typing import Annotated
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, UUID, text

from .permissions import UserRole, UserState
from ..models import Base
from .. import fields


str_128 = Annotated[str, mapped_column(String(128))]
uuid = Annotated[str, mapped_column(UUID())]


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[uuid] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str_128]
    role: Mapped[UserRole]
    state: Mapped[UserState]

    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]
