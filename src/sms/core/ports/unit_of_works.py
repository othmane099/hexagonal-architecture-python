from typing import Protocol

from src.sms.core.ports.repositories import (BrandRepository,
                                             CategoryRepository,
                                             RoleRepository, UserRepository)


class UnitOfWork(Protocol):
    brand_repository: BrandRepository
    user_repository: UserRepository
    role_repository: RoleRepository
    category_repository: CategoryRepository

    async def __aenter__(self) -> "UnitOfWork": ...

    async def __aexit__(self, exc_type, exc_val, traceback): ...

    async def commit(self): ...

    async def rollback(self): ...
