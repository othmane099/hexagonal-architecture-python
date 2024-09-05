import pytest

from src.sms.core.domain.dtos import CreateBrandDTO, IdsDTO, UpdateBrandDTO
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.helpers import SortDirection


@pytest.mark.asyncio(loop_scope="session")
async def test_create_brand(get_brand_service_impl, init_container):
    dto = CreateBrandDTO(
        name="service_brand_name", description="service_brand_description"
    )
    result = await get_brand_service_impl.create(dto)
    assert result.id is not None
    assert result.name == "service_brand_name"
    assert result.description == "service_brand_description"
    assert result.created_at is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_another_brand_with_existed_name(get_brand_service_impl):
    dto = CreateBrandDTO(name="service_brand_name", description=None)
    with pytest.raises(UniqueViolation):
        await get_brand_service_impl.create(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_find_all_brands(get_brand_service_impl):
    # Test order and sorting direction
    result = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="id", sort_dir=SortDirection.ASC
    )
    assert len(result.items) > 0
    assert result.items[0].id < result.items[-1].id
    result = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="id", sort_dir=SortDirection.DESC
    )
    assert len(result.items) > 0
    assert result.items[0].id > result.items[-1].id
    # change page
    result = await get_brand_service_impl.find_all(
        keyword=None, page=2, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert len(result.items) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_find_all_brands__search_by_keyword(get_brand_service_impl):
    dto = CreateBrandDTO(name="search_by_keyword", description=None)
    b1 = await get_brand_service_impl.create(dto)
    dto = CreateBrandDTO(
        name="search_by_keyword1", description="search_by_keyword_description"
    )
    b2 = await get_brand_service_impl.create(dto)
    result = await get_brand_service_impl.find_all(
        keyword=b1.name, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert len(result.items) == 2
    result = await get_brand_service_impl.find_all(
        keyword=b2.name, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert len(result.items) == 1
    result = await get_brand_service_impl.find_all(
        keyword="random",
        page=1,
        size=10,
        sort_column="name",
        sort_dir=SortDirection.ASC,
    )
    assert len(result.items) == 0
    result = await get_brand_service_impl.find_all(
        keyword="search_by_keyword_description",
        page=1,
        size=10,
        sort_column="name",
        sort_dir=SortDirection.ASC,
    )
    assert len(result.items) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_update_brand(get_brand_service_impl):
    # We should have just one
    existed_brands = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    brand = existed_brands.items[0]
    brand_id = brand.id
    # No data updated
    dto = UpdateBrandDTO(
        id=brand_id,
        name=brand.name,
        description=brand.description,
    )
    result = await get_brand_service_impl.update(dto)
    assert result == brand
    # Update name
    dto = UpdateBrandDTO(id=brand_id, name="test_brand2", description=brand.description)
    result = await get_brand_service_impl.update(dto)
    assert result.name == dto.name == "test_brand2"
    # Update description
    dto = UpdateBrandDTO(id=brand_id, name=result.name, description="test brand2")
    result = await get_brand_service_impl.update(dto)
    assert result.description == dto.description == "test brand2"
    # Update with not existed id
    dto = UpdateBrandDTO(id=99, name="test_brand2", description="test brand2")
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
    existed_brands_before_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    second_brand = existed_brands_before_delete.items[0]
    await get_brand_service_impl.delete(second_brand.id)
    existed_brands_after_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_brands_after_delete.items)
        == len(existed_brands_before_delete.items) - 1
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_all_by_ids(get_brand_service_impl):
    dto = CreateBrandDTO(name="test_delete_all_by_ids", description=None)
    b1 = await get_brand_service_impl.create(dto)
    dto = CreateBrandDTO(name="test_delete_all_by_ids1", description=None)
    b2 = await get_brand_service_impl.create(dto)
    dto = CreateBrandDTO(name="test_delete_all_by_ids2", description=None)
    b3 = await get_brand_service_impl.create(dto)
    ids = [b1.id, b2.id, b3.id, 999]
    dto = IdsDTO(ids=ids)
    existed_brands_before_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    result = await get_brand_service_impl.delete_all_by_ids(dto)
    existed_brands_after_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_brands_after_delete.items)
        == len(existed_brands_before_delete.items) - 3
    )
    assert result.not_existed_ids == [999]
    assert len(result.deleted_ids) == 3
    assert (
        b1.id in result.deleted_ids
        and b2.id in result.deleted_ids
        and b3.id in result.deleted_ids
    )
