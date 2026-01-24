from typing import Any, Callable

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.adapters.repositories.brand import BrandRepositoryImpl
from src.sms.adapters.repositories.category import CategoryRepositoryImpl
from src.sms.adapters.repositories.role import RoleRepositoryImpl
from src.sms.adapters.repositories.user import UserRepositoryImpl
from src.sms.core.ports.unit_of_works import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):
    @inject
    def __init__(
        self,
        session_factory: Callable[[], Any] = Provide["DEFAULT_SESSION_FACTORY"],
    ):
        self.session_factory = session_factory()
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session: AsyncSession = self.session_factory()
        self.brand_repository = BrandRepositoryImpl(self.session)
        self.user_repository = UserRepositoryImpl(self.session)
        self.role_repository = RoleRepositoryImpl(self.session)
        self.category_repository = CategoryRepositoryImpl(self.session)
        return self

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
