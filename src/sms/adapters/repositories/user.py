from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.sms.core.domain.models import User
from src.sms.core.ports.repositories import UserRepository


class UserRepositoryImpl(UserRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def find_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .filter_by(username=username)
            .filter_by(deleted_at=None)
            .options(joinedload(User.role))
        )
        return result.scalars().first()
