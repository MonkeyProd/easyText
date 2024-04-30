import dataclasses
import json
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
    print(config)
    port = f':{config.port}' if config.port else ''
    url = f"postgresql://{config.user}:{config.password}@{config.host}{port}/{config.database}"
    return url

