from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.auth import schemas
from app.auth.config import auth_settings
from app.auth.models import UserModel


ALGORITHM: str = 'HS256'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def create_access_token(user: UserModel, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRES_MINUTES))
    payload = schemas.TokenData.model_validate(user, from_attributes=True)
    payload.exp = expire

    encoded_jwt = jwt.encode(payload.model_dump(), auth_settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
