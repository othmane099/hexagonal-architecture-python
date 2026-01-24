from datetime import datetime

import pytest

from src.sms.adapters.repositories.fakes import (FakeCategoryRepository,
                                                 FakeUnitOfWork)
from src.sms.core.domain.dtos import (CreateCategoryDTO, IdsDTO,
                                      UpdateCategoryDTO)
from src.sms.core.domain.models import Category
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.core.services.category import CategoryServiceImpl


@pytest.fixture
def fake_uow():
    return FakeUnitOfWork()


@pytest.fixture
def category_service(fake_uow):
    return CategoryServiceImpl(unit_of_work=fake_uow)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_success(category_service, fake_uow):
    dto = CreateCategoryDTO(code="ELEC", name="Electronics")

    result = await category_service.create(dto)

    assert result.id == 1
    assert result.code == "ELEC"
    assert result.name == "Electronics"
    assert fake_uow.committed is True


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_duplicate_name_raises_unique_violation(category_service):
    dto = CreateCategoryDTO(code="ELEC", name="Electronics")
    await category_service.create(dto)

    dto2 = CreateCategoryDTO(code="ELEC2", name="Electronics")
    with pytest.raises(UniqueViolation, match="Category name should be UNIQUE"):
        await category_service.create(dto2)


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_id_success():
    category = Category(
        id=1,
        code="ELEC",
        name="Electronics",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeCategoryRepository(categories=[category])
    fake_uow = FakeUnitOfWork(category_repository=fake_repo)
    service = CategoryServiceImpl(unit_of_work=fake_uow)

    result = await service.find_by_id(1)

    assert result.id == 1
    assert result.code == "ELEC"
    assert result.name == "Electronics"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_id_not_found_raises_entity_not_found(category_service):
    with pytest.raises(EntityNotFound):
        await category_service.find_by_id(999)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_category_success():
    category = Category(
        id=1,
        code="ELEC",
        name="Electronics",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeCategoryRepository(categories=[category])
    fake_uow = FakeUnitOfWork(category_repository=fake_repo)
    service = CategoryServiceImpl(unit_of_work=fake_uow)

    dto = UpdateCategoryDTO(id=1, code="ELEC2", name="Electronics Updated")
    result = await service.update(dto)

    assert result.code == "ELEC2"
    assert result.name == "Electronics Updated"
    assert fake_uow.committed is True


@pytest.mark.asyncio(loop_scope="session")
async def test_update_category_duplicate_code_raises_unique_violation():
    category1 = Category(
        id=1,
        code="ELEC",
        name="Electronics",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    category2 = Category(
        id=2,
        code="CLOTH",
        name="Clothing",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeCategoryRepository(categories=[category1, category2])
    fake_uow = FakeUnitOfWork(category_repository=fake_repo)
    service = CategoryServiceImpl(unit_of_work=fake_uow)

    dto = UpdateCategoryDTO(id=1, code="CLOTH", name="Electronics")

    with pytest.raises(UniqueViolation, match="Brand code should be UNIQUE"):
        await service.update(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_category_duplicate_name_raises_unique_violation():
    category1 = Category(
        id=1,
        code="ELEC",
        name="Electronics",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    category2 = Category(
        id=2,
        code="CLOTH",
        name="Clothing",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeCategoryRepository(categories=[category1, category2])
    fake_uow = FakeUnitOfWork(category_repository=fake_repo)
    service = CategoryServiceImpl(unit_of_work=fake_uow)

    dto = UpdateCategoryDTO(id=1, code="ELEC", name="Clothing")

    with pytest.raises(UniqueViolation, match="Brand name should be UNIQUE"):
        await service.update(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_success():
    category = Category(
        id=1,
        code="ELEC",
        name="Electronics",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeCategoryRepository(categories=[category])
    fake_uow = FakeUnitOfWork(category_repository=fake_repo)
    service = CategoryServiceImpl(unit_of_work=fake_uow)

    await service.delete(1)

    assert category.deleted_at is not None
    assert fake_uow.committed is True


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_not_found_raises_entity_not_found(category_service):
    with pytest.raises(EntityNotFound):
        await category_service.delete(999)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_all_by_ids_success():
    category1 = Category(
        id=1,
        code="ELEC",
        name="Electronics",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    category2 = Category(
        id=2,
        code="CLOTH",
        name="Clothing",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeCategoryRepository(categories=[category1, category2])
    fake_uow = FakeUnitOfWork(category_repository=fake_repo)
    service = CategoryServiceImpl(unit_of_work=fake_uow)

    dto = IdsDTO(ids=[1, 2, 999])
    result = await service.delete_all_by_ids(dto)

    assert result.deleted_ids == [1, 2]
    assert result.not_existed_ids == [999]
    assert category1.deleted_at is not None
    assert category2.deleted_at is not None
