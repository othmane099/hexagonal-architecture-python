from src.sms.core.domain.models import User
from src.sms.core.ports.repositories import UserRepository


class FakeUserRepository(UserRepository):

    def __init__(self, users: list[User] | None = None):
        self._users: list[User] = users if users is not None else []

    async def find_by_username(self, username: str) -> User | None:
        for user in self._users:
            if user.username == username and user.deleted_at is None:
                return user
        return None
