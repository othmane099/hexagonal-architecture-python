from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.core.domain.models import Category
from src.sms.core.ports.repositories import CategoryRepository
from src.sms.helpers import SortDirection, get_column, order_by_column


class CategoryRepositoryImpl(CategoryRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    def create(self, category: Category) -> None:
        self.session.add(category)

    async def find_by_id(self, category_id: int) -> Category | None:
        result = await self.session.execute(
            select(Category).filter_by(id=category_id).filter_by(deleted_at=None)
        )
        return result.scalars().first()

    async def find_by_name(self, name: str) -> Category | None:
        result = await self.session.execute(
            select(Category).filter_by(name=name).filter_by(deleted_at=None)
        )
        return result.scalars().first()

    async def find_by_code(self, code: str) -> Category | None:
        result = await self.session.execute(
            select(Category).filter_by(code=code).filter_by(deleted_at=None)
        )
        return result.scalars().first()

    def get_find_all_stmt(
        self, keyword: str | None, sort_column: str, direction: SortDirection
    ) -> Select[tuple[Category]]:
        stmt = select(Category).filter_by(deleted_at=None)

        if keyword:
            stmt = stmt.filter(
                or_(
                    Category.name.ilike(f"%{keyword}%"),
                    Category.code.ilike(f"%{keyword}%"),
                )
            )
        column = get_column(Category, sort_column)
        if column:
            stmt = stmt.order_by(order_by_column(column, direction))

        return stmt

    async def find_all_by_ids(self, ids: list[int]) -> list[Category]:
        result = await self.session.execute(
            select(Category).where(Category.id.in_(ids), Category.deleted_at.is_(None))
        )
        return result.scalars().all()
