import multiprocessing
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from sqlalchemy.testing.plugin.plugin_base import logging

USER = 'postgres'
PASSWORD = 'newpassword'

class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None
    postgres_dsn: PostgresDsn = MultiHostUrl(f'postgresql+asyncpg://{USER}:{PASSWORD}@localhost/sf_be')
    jwt_secret: str = "secret"
    algorithm: list = ['HS256']

    class Config:
        _env_file = ".env"
        _extra = 'allow'

app_settings = AppSettings()

# набор опций для запуска сервера
uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload
}

