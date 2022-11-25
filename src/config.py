import os
import logging
from functools import lru_cache

from rich.console import Console
from rich.logging import RichHandler

from pydantic import BaseSettings

console = Console(color_system="256", width=200, style="blue")


@lru_cache()
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    handler = RichHandler(rich_tracebacks=True, console=console, tracebacks_show_locals=True)
    handler.setFormatter(logging.Formatter("[ %(threadName)s:%(funcName)s:%(lineno)d ] - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


class Settings(BaseSettings):
    pg_user: str = os.getenv("DB_USER", "postgres")
    pg_pass: str = os.getenv("PASSWORD", "postgres")
    pg_host: str = os.getenv("HOST", "localhost")
    pg_port: str = os.getenv("PORT", '5432')
    pg_database: str = os.getenv("DB", "flow")

    jwt_secret_key: str = os.getenv("SECRET_KEY", "17a04cf8d9d99cfca9dad2813b06c6424f5c9d551c0d804eb02eeee7875c4dcb")
    jwt_algorithm: str = os.getenv("ALGORITHM", "HS256")
    jwt_access_toke_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60*60)


settings = Settings()


DB_CONF = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': settings.pg_host,
                'port': settings.pg_port,
                'user': settings.pg_user,
                'password': settings.pg_pass,
                'database': settings.pg_database,
            }
        },
    },
    'apps': {
        'models': {
            'models': [
                 'apps.flow.models', 'apps.applications.models', 'apps.applicant.models', 'aerich.models'
            ],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}


