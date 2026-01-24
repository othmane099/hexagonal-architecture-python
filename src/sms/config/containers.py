from dependency_injector import containers, providers

from src.sms.adapters.db.core import default_session_factory
from src.sms.adapters.unit_of_works import UnitOfWorkImpl
from src.sms.core.services.brand import BrandServiceImpl
from src.sms.core.services.category import CategoryServiceImpl
from src.sms.core.services.security import AuthenticationServiceImpl
from src.sms.core.services.user import UserServiceImpl


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src.sms"],
    )

    DEFAULT_SESSION_FACTORY = default_session_factory

    unit_of_work = providers.Factory(
        UnitOfWorkImpl, session_factory=DEFAULT_SESSION_FACTORY
    )

    brand_service_impl = providers.Factory(
        BrandServiceImpl,
        unit_of_work=unit_of_work,
    )

    category_service_impl = providers.Factory(
        CategoryServiceImpl,
        unit_of_work=unit_of_work,
    )

    user_service_impl = providers.Factory(
        UserServiceImpl,
        unit_of_work=unit_of_work,
    )

    authentication_service_impl = providers.Factory(AuthenticationServiceImpl)
