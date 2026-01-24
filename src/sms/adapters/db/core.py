from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.sms.config.settings import get_database_uri

db_uri = get_database_uri()
ENGINE = create_async_engine(db_uri)


def default_session_factory():
    return async_sessionmaker(
        bind=ENGINE, autocommit=False, expire_on_commit=False, class_=AsyncSession
    )
