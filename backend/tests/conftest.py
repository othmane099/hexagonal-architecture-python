import pytest
import pytest_asyncio

from src.sms.adapters.db.orm import metadata, start_mappers
from src.sms.config.containers import ENGINE, Container
from src.sms.core.services.brand import BrandServiceImpl


@pytest_asyncio.fixture(scope="session")
async def get_container():
    async with ENGINE.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        start_mappers()
    return Container()


@pytest.fixture
def get_brand_service_impl():
    return BrandServiceImpl()
