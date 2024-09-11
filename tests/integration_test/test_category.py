import pytest

from src.sms.core.domain.dtos import (CreateCategoryDTO, IdsDTO,
                                      UpdateCategoryDTO)
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.helpers import SortDirection


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category(get_category_service_impl):
    dto = CreateCategoryDTO(name="service_category_name", code="service_category_code")
    result = await get_category_service_impl.create(dto)
    assert result.id is not None
    assert result.name == "service_category_name"
    assert result.code == "service_category_code"
    assert result.created_at is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_another_category_with_existed_name(get_category_service_impl):
    dto = CreateCategoryDTO(
        name="service_category_name", code="service_category_name_code"
    )
    with pytest.raises(UniqueViolation):
        await get_category_service_impl.create(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_find_all_categories(get_category_service_impl):
    # Test order and sorting direction
    result = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="id", sort_dir=SortDirection.ASC
    )
    assert len(result.items) > 0
    assert result.items[0].id < result.items[-1].id
    result = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="id", sort_dir=SortDirection.DESC
    )
    assert len(result.items) > 0
    assert result.items[0].id > result.items[-1].id
    # change page
    result = await get_category_service_impl.find_all(
        keyword=None, page=2, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert len(result.items) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_find_all_categories__search_by_keyword(get_category_service_impl):
    dto = CreateCategoryDTO(name="search_by_keyword", code="search_by_keyword_code")
    b1 = await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(name="search_by_keyword1", code="search_by_keyword1_code")
    b2 = await get_category_service_impl.create(dto)
    result = await get_category_service_impl.find_all(
        keyword=b1.name, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert len(result.items) == 2
    result = await get_category_service_impl.find_all(
        keyword=b2.name, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert len(result.items) == 1
    result = await get_category_service_impl.find_all(
        keyword="random",
        page=1,
        size=10,
        sort_column="name",
        sort_dir=SortDirection.ASC,
    )
    assert len(result.items) == 0
    result = await get_category_service_impl.find_all(
        keyword="search_by_keyword_code",
        page=1,
        size=10,
        sort_column="name",
        sort_dir=SortDirection.ASC,
    )
    assert len(result.items) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_update_category(get_category_service_impl):
    # We should have just one
    existed_categories = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    category = existed_categories.items[0]
    category_id = category.id
    # No data updated
    dto = UpdateCategoryDTO(
        id=category_id,
        name=category.name,
        code=category.code,
    )
    result = await get_category_service_impl.update(dto)
    assert result == category
    # Update name
    dto = UpdateCategoryDTO(id=category_id, name="test_category2", code=category.code)
    result = await get_category_service_impl.update(dto)
    assert result.name == dto.name == "test_category2"
    # Update code
    dto = UpdateCategoryDTO(id=category_id, name=result.name, code="test category2")
    result = await get_category_service_impl.update(dto)
    assert result.code == dto.code == "test category2"
    # Update with not existed id
    dto = UpdateCategoryDTO(id=99, name="test_category2", code="test category2")
    with pytest.raises(EntityNotFound):
        await get_category_service_impl.update(dto)

    # Update category with duplicated name (existed name)
    dto = CreateCategoryDTO(name="test_category3", code="test category3")
    second_category = await get_category_service_impl.create(dto)

    dto = UpdateCategoryDTO(
        id=second_category.id, name="test_category2", code=second_category.code
    )
    with pytest.raises(UniqueViolation):
        await get_category_service_impl.update(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_the_second_category(get_category_service_impl):
    existed_categories_before_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    second_category = existed_categories_before_delete.items[0]
    await get_category_service_impl.delete(second_category.id)
    existed_categories_after_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_categories_after_delete.items)
        == len(existed_categories_before_delete.items) - 1
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_all_by_ids(get_category_service_impl):
    dto = CreateCategoryDTO(
        name="test_delete_all_by_ids0", code="test_delete_all_by_ids0_code"
    )
    b1 = await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(
        name="test_delete_all_by_ids10", code="test_delete_all_by_ids1_code1"
    )
    b2 = await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(
        name="test_delete_all_by_ids20", code="test_delete_all_by_ids2_code2"
    )
    b3 = await get_category_service_impl.create(dto)
    ids = [b1.id, b2.id, b3.id, 999]
    dto = IdsDTO(ids=ids)
    existed_categories_before_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    result = await get_category_service_impl.delete_all_by_ids(dto)
    existed_categories_after_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_categories_after_delete.items)
        == len(existed_categories_before_delete.items) - 3
    )
    assert result.not_existed_ids == [999]
    assert len(result.deleted_ids) == 3
    assert (
        b1.id in result.deleted_ids
        and b2.id in result.deleted_ids
        and b3.id in result.deleted_ids
    )
