from datetime import datetime

from src.sms.core.domain.models import Category
from src.sms.core.ports.repositories import CategoryRepository


class FakeCategoryRepository(CategoryRepository):

    def __init__(self, categories: list[Category] | None = None):
        self._categories: list[Category] = categories if categories is not None else []
        self._id_counter = 1

    def create(self, category: Category) -> None:
        if category.id is None:
            category.id = self._id_counter
            self._id_counter += 1
        if category.created_at is None:
            category.created_at = datetime.now()
        self._categories.append(category)

    async def find_by_id(self, id_: int) -> Category | None:
        for category in self._categories:
            if category.id == id_ and category.deleted_at is None:
                return category
        return None

    async def find_by_name(self, name: str) -> Category | None:
        for category in self._categories:
            if category.name == name and category.deleted_at is None:
                return category
        return None

    async def find_by_code(self, code: str) -> Category | None:
        for category in self._categories:
            if category.code == code and category.deleted_at is None:
                return category
        return None

    async def find_all_by_ids(self, ids: list[int]) -> list[Category]:
        return [
            category
            for category in self._categories
            if category.id in ids and category.deleted_at is None
        ]
