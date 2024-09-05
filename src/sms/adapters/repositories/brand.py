from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.core.domain.models import Brand
from src.sms.core.ports.repositories import BrandRepository
from src.sms.helpers import SortDirection, get_column, order_by_column


class BrandRepositoryImpl(BrandRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    def create(self, brand: Brand) -> None:
        self.session.add(brand)

    async def find_by_id(self, brand_id: int) -> Brand | None:
        result = await self.session.execute(
            select(Brand).filter_by(id=brand_id).filter_by(deleted_at=None)
        )
        return result.scalars().first()

    async def find_by_name(self, name: str) -> Brand | None:
        result = await self.session.execute(
            select(Brand).filter_by(name=name).filter_by(deleted_at=None)
        )
        return result.scalars().first()

    def get_find_all_stmt(
        self, keyword: str | None, sort_column: str, direction: SortDirection
    ) -> Select[tuple[Brand]]:
        stmt = select(Brand).filter_by(deleted_at=None)

        if keyword:
            stmt = stmt.filter(
                or_(
                    Brand.name.ilike(f"%{keyword}%"),
                    Brand.description.ilike(f"%{keyword}%"),
                )
            )
        column = get_column(Brand, sort_column)
        if column:
            stmt = stmt.order_by(order_by_column(column, direction))

        return stmt

    async def find_all_by_ids(self, ids: list[int]) -> list[Brand]:
        result = await self.session.execute(
            select(Brand).where(Brand.id.in_(ids), Brand.deleted_at.is_(None))
        )
        return result.scalars().all()
