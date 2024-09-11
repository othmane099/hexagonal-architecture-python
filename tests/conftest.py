import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.adapters.db.orm import metadata, start_mappers
from src.sms.config.containers import ENGINE, Container
from src.sms.core.domain.models import Permission, Role, User
from src.sms.core.ports.services import CategoryService
from src.sms.core.services.brand import BrandServiceImpl
from src.sms.core.services.category import CategoryServiceImpl
from src.sms.core.services.security import hash_password
from src.sms.core.services.user import UserServiceImpl


@pytest_asyncio.fixture(scope="session")
async def drop_and_create_database():
    async with ENGINE.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def init_container():
    return Container()


@pytest_asyncio.fixture(scope="session")
async def get_container():
    async with ENGINE.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        start_mappers()
    return Container()


@pytest_asyncio.fixture(scope="session")
async def init_owner():
    async with AsyncSession(ENGINE) as session:
        brand_perm = Permission(
            id=None,
            name="brand",
            label="Brand",
            description="Brand permission",
            created_at=None,
            updated_at=None,
            deleted_at=None,
        )
        category_perm = Permission(
            id=None,
            name="category",
            label="Category",
            description="Category permission",
            created_at=None,
            updated_at=None,
            deleted_at=None,
        )
        role = Role(
            id=None,
            name="owner",
            label="Owner",
            description="Owner role",
            created_at=None,
            updated_at=None,
            deleted_at=None,
        )
        role.permissions.extend([brand_perm, category_perm])
        session.add(role)
        await session.commit()
        new_user = User(
            id=None,
            role_id=1,
            firstname="test_owner",
            lastname="test_owner",
            username="test_owner",
            email="test_owner@example.com",
            password=hash_password("123456"),
            phone="0123456789",
            is_active=True,
            created_at=None,
            updated_at=None,
            deleted_at=None,
            role=role,
        )
        session.add(new_user)
        await session.commit()


@pytest.fixture
def get_brand_service_impl():
    return BrandServiceImpl()


@pytest.fixture(scope="session")
def get_user_service_impl():
    return UserServiceImpl()


@pytest.fixture(scope="session")
def get_category_service_impl():
    return CategoryServiceImpl()
