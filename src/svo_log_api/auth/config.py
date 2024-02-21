from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / '.env')

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int


auth_settings = AuthSettings()
