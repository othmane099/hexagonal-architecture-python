from src.sms.adapters.repositories.fakes.brand import FakeBrandRepository
from src.sms.adapters.repositories.fakes.category import FakeCategoryRepository
from src.sms.adapters.repositories.fakes.role import FakeRoleRepository
from src.sms.adapters.repositories.fakes.user import FakeUserRepository
from src.sms.core.ports.unit_of_works import UnitOfWork


class FakeUnitOfWork(UnitOfWork):

    def __init__(
        self,
        brand_repository: FakeBrandRepository | None = None,
        category_repository: FakeCategoryRepository | None = None,
        user_repository: FakeUserRepository | None = None,
        role_repository: FakeRoleRepository | None = None,
    ):
        self.brand_repository = brand_repository or FakeBrandRepository()
        self.category_repository = category_repository or FakeCategoryRepository()
        self.user_repository = user_repository or FakeUserRepository()
        self.role_repository = role_repository or FakeRoleRepository()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type:
            await self.rollback()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True
