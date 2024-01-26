from pydantic import BaseModel, Field
from configparser import ConfigParser
from pathlib import Path


class Settings(BaseModel):
    DB_HOST: str = Field(alias='db_host')
    DB_PORT: str = Field(alias='db_port')
    DB_USER: str = Field(alias='db_user')
    DB_PASS: str = Field(alias='db_pass')
    DB_NAME: str = Field(alias='db_name')

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = ConfigParser()
config.read(Path(__file__).parent / 'env.ini')
settings = Settings(**config['DataBase'])



