from abc import ABC, ABCMeta, abstractmethod

from src.sms.core.ports.repositories import (BrandRepository,
                                             CategoryRepository,
                                             RoleRepository, UserRepository)


class UnitOfWork(ABC, metaclass=ABCMeta):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class BrandUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: BrandRepository


class UserUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: UserRepository


class RoleUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: RoleRepository


class CategoryUnitOfWork(UnitOfWork, metaclass=ABCMeta):
    repository: CategoryRepository
