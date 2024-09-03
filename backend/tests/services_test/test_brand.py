import pytest

from src.sms.core.domain.dtos import CreateBrandDTO


@pytest.mark.asyncio(loop_scope="session")
async def test_create_brand(get_brand_service_impl, get_container):
    dto = CreateBrandDTO(name="test_brand", description="test brand")
    result = await get_brand_service_impl.create(dto)
    assert result.id is not None
    assert result.name == "test_brand"
    assert result.description == "test brand"
    assert result.created_at is not None
