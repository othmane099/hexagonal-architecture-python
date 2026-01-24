from datetime import datetime

import pytest

from src.sms.adapters.repositories.fakes import (FakeUnitOfWork,
                                                 FakeUserRepository)
from src.sms.core.domain.models import Role, User
from src.sms.core.exceptions import EntityNotFound
from src.sms.core.services.user import UserServiceImpl


@pytest.fixture
def fake_uow():
    return FakeUnitOfWork()


@pytest.fixture
def user_service(fake_uow):
    return UserServiceImpl(unit_of_work=fake_uow)


def create_test_user(
    id_: int = 1,
    username: str = "testuser",
    email: str = "test@example.com",
) -> User:
    role = Role(
        id=1,
        name="admin",
        label="Administrator",
        description="Admin role",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    return User(
        id=id_,
        role_id=1,
        firstname="Test",
        lastname="User",
        username=username,
        email=email,
        password="hashedpassword",
        phone="1234567890",
        is_active=True,
        role=role,
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_username_success():
    user = create_test_user()
    fake_repo = FakeUserRepository(users=[user])
    fake_uow = FakeUnitOfWork(user_repository=fake_repo)
    service = UserServiceImpl(unit_of_work=fake_uow)

    result = await service.find_by_username("testuser")

    assert result.id == 1
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.firstname == "Test"
    assert result.lastname == "User"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_username_not_found_raises_entity_not_found(user_service):
    with pytest.raises(EntityNotFound, match="User not found with given username"):
        await user_service.find_by_username("nonexistent")


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_username_ignores_deleted_users():
    user = create_test_user()
    user.deleted_at = datetime.now()
    fake_repo = FakeUserRepository(users=[user])
    fake_uow = FakeUnitOfWork(user_repository=fake_repo)
    service = UserServiceImpl(unit_of_work=fake_uow)

    with pytest.raises(EntityNotFound, match="User not found with given username"):
        await service.find_by_username("testuser")
