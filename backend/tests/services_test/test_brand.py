import pytest

from src.sms.core.domain.dtos import CreateBrandDTO, UpdateBrandDTO
from src.sms.core.exceptions import UniqueViolation, EntityNotFound


@pytest.mark.asyncio(loop_scope="session")
async def test_create_brand(get_brand_service_impl, get_container):
    dto = CreateBrandDTO(name="test_brand", description="test brand")
    result = await get_brand_service_impl.create(dto)
    assert result.id is not None
    assert result.name == "test_brand"
    assert result.description == "test brand"
    assert result.created_at is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_another_brand_with_existed_name(get_brand_service_impl):
    dto = CreateBrandDTO(name="test_brand", description=None)
    with pytest.raises(UniqueViolation):
        await get_brand_service_impl.create(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_find_all_brands(get_brand_service_impl):
    result = await get_brand_service_impl.find_all(page=1, size=2)
    assert len(result.items) > 0
    # we have just one brand
    result = await get_brand_service_impl.find_all(page=2, size=2)
    assert len(result.items) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_update_brand(get_brand_service_impl):
    # We should have just one
    existed_brands = await get_brand_service_impl.find_all(page=1, size=2)
    the_only_brand = existed_brands.items[0]
    the_only_brand_id = the_only_brand.id
    # No data updated
    dto = UpdateBrandDTO(
        id=the_only_brand_id, name="test_brand", description="test brand"
    )
    result = await get_brand_service_impl.update(dto)
    assert result == the_only_brand
    # Update name
    dto = UpdateBrandDTO(
        id=the_only_brand_id, name="test_brand2", description="test brand"
    )
    result = await get_brand_service_impl.update(dto)
    assert result.name == dto.name == "test_brand2"
    # Update description
    dto = UpdateBrandDTO(
        id=the_only_brand_id, name="test_brand2", description="test brand2"
    )
    result = await get_brand_service_impl.update(dto)
    assert result.description == dto.description == "test brand2"
    # Update with not existed id
    dto = UpdateBrandDTO(
        id=99, name="test_brand2", description="test brand2"
    )
    with pytest.raises(EntityNotFound):
        await get_brand_service_impl.update(dto)

    # Update brand with duplicated name (existed name)
    dto = CreateBrandDTO(name="test_brand3", description="test brand3")
    second_brand = await get_brand_service_impl.create(dto)

    dto = UpdateBrandDTO(
        id=second_brand.id, name="test_brand2", description=second_brand.description
    )
    with pytest.raises(UniqueViolation):
        await get_brand_service_impl.update(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_the_second_brand(get_brand_service_impl):
    second_brand = await get_brand_service_impl.find_by_id(2)
    await get_brand_service_impl.delete(second_brand.id)
    existed_brands = await get_brand_service_impl.find_all(page=1, size=2)
    assert len(existed_brands.items) == 1
