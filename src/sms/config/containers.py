from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.sms.adapters.unit_of_works import (BrandUnitOfWorkImpl,
                                            UserUnitOfWorkImpl)
from src.sms.config.settings import get_database_uri
from src.sms.core.services.brand import BrandServiceImpl
from src.sms.core.services.user import UserServiceImpl

db_uri = get_database_uri()
ENGINE = create_async_engine(db_uri)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src.sms"],
    )

    DEFAULT_SESSION_FACTORY = lambda: async_sessionmaker(
        bind=ENGINE, autocommit=False, expire_on_commit=False, class_=AsyncSession
    )

    brand_unit_of_work = providers.Factory(
        BrandUnitOfWorkImpl, session_factory=DEFAULT_SESSION_FACTORY
    )

    brand_service_impl = providers.Factory(
        BrandServiceImpl,
        brand_unit_of_work=brand_unit_of_work,
    )

    user_unit_of_work = providers.Factory(
        UserUnitOfWorkImpl, session_factory=DEFAULT_SESSION_FACTORY
    )

    user_service_impl = providers.Factory(
        UserServiceImpl,
        user_unit_of_work=user_unit_of_work,
    )
