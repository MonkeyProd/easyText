import dataclasses
import json
import os
from os import environ

# 3 hours in seconds
TOKEN_EXPIRE_DELTA_SECONDS = 3 * 60 * 60

@dataclasses.dataclass
class PostgresConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


def make_url() -> str:
    config = PostgresConfig('database', 5432, 'postgres', 'postgres', 'postgres')
    is_in_docker = os.environ.get('DEV') is not None
    if not is_in_docker:
        config.host = 'localhost'

    print(f'Starting in docker: {is_in_docker}.\n', config)
    port = f':{config.port}' if config.port else ''
    url = f"postgresql://{config.user}:{config.password}@{config.host}{port}/{config.database}"
    return url

