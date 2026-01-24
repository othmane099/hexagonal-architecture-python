from typing import Protocol

from sqlalchemy import Select

from src.sms.core.domain.models import Brand, Category, Role, User
from src.sms.helpers import SortDirection


class BrandRepository(Protocol):
    def create(self, brand: Brand) -> None: ...

    async def find_by_id(self, id_: int) -> Brand | None: ...

    async def find_by_name(self, name: str) -> Brand | None: ...

    def get_find_all_stmt(
        self, keyword: str | None, sort_column: str, direction: SortDirection
    ) -> Select[tuple[Brand]]: ...

    async def find_all_by_ids(self, ids: list[int]) -> list[Brand]: ...


class UserRepository(Protocol):

    async def find_by_username(self, username: str) -> User | None: ...


class RoleRepository(Protocol):

    async def find_by_name(self, name: str) -> Role | None: ...

    async def role_has_permission(self, role_name: str, permission_name: str) -> bool:
        """Check if a role has a permission."""
        ...


class CategoryRepository(Protocol):
    def create(self, category: Category) -> None: ...

    async def find_by_id(self, id_: int) -> Category | None: ...

    async def find_by_name(self, name: str) -> Category | None: ...

    def get_find_all_stmt(
        self, keyword: str | None, sort_column: str, direction: SortDirection
    ) -> Select[tuple[Category]]: ...

    async def find_all_by_ids(self, ids: list[int]) -> list[Category]: ...

    async def find_by_code(self, code: str) -> Category | None: ...
