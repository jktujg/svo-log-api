from secrets import token_urlsafe

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.prod.env'),
        env_ignore_empty=False,
        extra='ignore'
    )

    SECRET_KEY: str = token_urlsafe(32)
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 1440


auth_settings = AuthSettings()
