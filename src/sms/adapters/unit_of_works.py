from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.adapters.repositories.brand import BrandRepositoryImpl
from src.sms.adapters.repositories.user import UserRepositoryImpl
from src.sms.core.ports.unit_of_works import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):

    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class BrandUnitOfWorkImpl(UnitOfWorkImpl):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = BrandRepositoryImpl(self.session)
        return self


class UserUnitOfWorkImpl(UnitOfWorkImpl):

    async def __aenter__(self):
        await super().__aenter__()
        self.repository = UserRepositoryImpl(self.session)
        return self
