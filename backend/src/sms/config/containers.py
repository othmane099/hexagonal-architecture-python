from dependency_injector import containers
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.sms.config.settings import get_database_uri

db_uri = get_database_uri()
ENGINE = create_async_engine(db_uri)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src.sms"],
    )

    DEFAULT_SESSION_FACTORY = lambda: async_sessionmaker(
        bind=ENGINE, autocommit=False, expire_on_commit=False, class_=AsyncSession
    )
