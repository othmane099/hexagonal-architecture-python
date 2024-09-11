from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.core.domain.models import Permission, Role
from src.sms.core.ports.repositories import RoleRepository


class RoleRepositoryImpl(RoleRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def find_by_name(self, name: str) -> Role | None:
        result = await self.session.execute(
            select(Role).filter_by(name=name).filter_by(deleted_at=None)
        )
        return result.scalars().first()

    async def role_has_permission(self, role_name: str, permission_name: str) -> bool:
        """Check if a role has a permission."""
        stmt = (
            select(1)
            .select_from(Role)
            .join(Role.permissions)
            .where(Role.name == role_name)
            .where(Permission.name == permission_name)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        result = result.scalar()
        return result is not None
