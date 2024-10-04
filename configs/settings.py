from typing import List, Union
from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    S3_BUCKET: str
    BUCKET_PREFIX: str

    PG_USER: str
    PG_PWD: str
    PG_ENDPOINT: str
    PG_DATABASE: str
    PG_PORT: str
    PG_SCHEMA: str

    # PROJECT_BASE_PATH: str = str(pathlib.Path(__file__).parent.parent.parent.absolute())
    EXCHANGE: str
    EXCHANGE_TYPE: str
    EXCHANGE_ROUTING_KEY: str
    EXCHANGE_USER: str
    EXCHANGE_PASSWORD: str
    EXCHANGE_IP: str
    EXCHANGE_VIRTUALHOST: str


settings = Settings()
