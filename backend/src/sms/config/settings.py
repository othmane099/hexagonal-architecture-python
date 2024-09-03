import os


class Settings:
    if os.getenv("TEST_RUN"):
        db_uri = "postgresql+asyncpg://test:test@localhost:5436/test"
    else:
        db_uri = "postgresql+asyncpg://postgres:postgres@localhost:5435/postgres"


def get_database_uri() -> str:
    return Settings.db_uri