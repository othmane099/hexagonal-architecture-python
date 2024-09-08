import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.adapters.db.orm import metadata, start_mappers
from src.sms.config.containers import ENGINE, Container
from src.sms.core.domain.models import User
from src.sms.core.services.brand import BrandServiceImpl
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
        new_user = User(
            id=None,  # Replace with appropriate values
            firstname="test_owner",
            lastname="test_owner",
            username="test_owner",
            email="test_owner@example.com",
            password="123",
            phone="0123456789",
            is_active=True,
            created_at=None,
            updated_at=None,
            deleted_at=None,
        )
        session.add(new_user)
        await session.commit()


@pytest.fixture
def get_brand_service_impl():
    return BrandServiceImpl()


@pytest.fixture
def get_user_service_impl():
    return UserServiceImpl()
