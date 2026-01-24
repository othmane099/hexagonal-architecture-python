from abc import ABCMeta
from typing import Protocol

from src.sms.core.ports.repositories import (BrandRepository,
                                             CategoryRepository,
                                             RoleRepository, UserRepository)


class UnitOfWork(Protocol):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()

    async def commit(self):
        ...

    async def rollback(self):
        ...


class BrandUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: BrandRepository


class UserUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: UserRepository


class RoleUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: RoleRepository


class CategoryUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: CategoryRepository
