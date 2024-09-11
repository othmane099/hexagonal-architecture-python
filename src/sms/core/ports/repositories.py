from abc import ABC, abstractmethod

from sqlalchemy import Select

from src.sms.core.domain.models import Brand, Category, Role, User
from src.sms.helpers import SortDirection


class BrandRepository(ABC):
    @abstractmethod
    def create(self, brand: Brand) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id_: int) -> Brand | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_name(self, name: str) -> Brand | None:
        raise NotImplementedError

    @abstractmethod
    def get_find_all_stmt(
        self, keyword: str | None, sort_column: str, direction: SortDirection
    ) -> Select[tuple[Brand]]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_ids(self, ids: list[int]) -> list[Brand]:
        raise NotImplementedError


class UserRepository(ABC):

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        raise NotImplementedError


class RoleRepository(ABC):

    @abstractmethod
    async def find_by_name(self, name: str) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    async def role_has_permission(self, role_name: str, permission_name: str) -> bool:
        """Check if a role has a permission."""
        raise NotImplementedError


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id_: int) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_name(self, name: str) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def get_find_all_stmt(
        self, keyword: str | None, sort_column: str, direction: SortDirection
    ) -> Select[tuple[Category]]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_ids(self, ids: list[int]) -> list[Category]:
        raise NotImplementedError
