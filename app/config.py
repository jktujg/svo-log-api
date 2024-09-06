import warnings
from typing import Self

from pydantic import model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.prod.env'),
        env_ignore_empty=False,
        extra='ignore',
    )

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    ROOT_PATH: str = '/api/v1'
    AIRPORT_PATH: str = ''
    AUTH_PATH: str = '/auth'

    LOG_LEVEL: str = 'DEBUG'

    @property
    def DB_URI(self):
        return MultiHostUrl.build(
            scheme='postgresql+psycopg',
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    @model_validator(mode='after')
    def _check_defaults(self) -> Self:
        for field_name in self.model_fields:
            if getattr(self, field_name) == 'changethis':
                warnings.warn(
                    message=f'The value of {field_name} is "changethis", '
                            "for security, please change it, at least for deployments.",
                    stacklevel=1,
                )

        return self


settings = Settings()
