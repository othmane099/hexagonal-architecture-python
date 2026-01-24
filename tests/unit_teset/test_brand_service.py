from datetime import datetime

import pytest

from src.sms.adapters.repositories.fakes import (FakeBrandRepository,
                                                 FakeUnitOfWork)
from src.sms.core.domain.dtos import CreateBrandDTO, IdsDTO, UpdateBrandDTO
from src.sms.core.domain.models import Brand
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.core.services.brand import BrandServiceImpl


@pytest.fixture
def fake_uow():
    return FakeUnitOfWork()


@pytest.fixture
def brand_service(fake_uow):
    return BrandServiceImpl(unit_of_work=fake_uow)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_brand_success(brand_service, fake_uow):
    dto = CreateBrandDTO(name="Nike", description="Sports brand")

    result = await brand_service.create(dto)

    assert result.id == 1
    assert result.name == "Nike"
    assert result.description == "Sports brand"
    assert fake_uow.committed is True


@pytest.mark.asyncio(loop_scope="session")
async def test_create_brand_duplicate_name_raises_unique_violation(brand_service):
    dto = CreateBrandDTO(name="Nike", description="Sports brand")
    await brand_service.create(dto)

    with pytest.raises(UniqueViolation, match="Brand name should be UNIQUE"):
        await brand_service.create(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_id_success():
    brand = Brand(
        id=1,
        name="Adidas",
        description="Sports brand",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeBrandRepository(brands=[brand])
    fake_uow = FakeUnitOfWork(brand_repository=fake_repo)
    service = BrandServiceImpl(unit_of_work=fake_uow)

    result = await service.find_by_id(1)

    assert result.id == 1
    assert result.name == "Adidas"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_by_id_not_found_raises_entity_not_found(brand_service):
    with pytest.raises(EntityNotFound):
        await brand_service.find_by_id(999)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_brand_success():
    brand = Brand(
        id=1,
        name="Nike",
        description="Old description",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeBrandRepository(brands=[brand])
    fake_uow = FakeUnitOfWork(brand_repository=fake_repo)
    service = BrandServiceImpl(unit_of_work=fake_uow)

    dto = UpdateBrandDTO(id=1, name="Nike Updated", description="New description")
    result = await service.update(dto)

    assert result.name == "Nike Updated"
    assert result.description == "New description"
    assert fake_uow.committed is True


@pytest.mark.asyncio(loop_scope="session")
async def test_update_brand_duplicate_name_raises_unique_violation():
    brand1 = Brand(
        id=1,
        name="Nike",
        description="Desc1",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    brand2 = Brand(
        id=2,
        name="Adidas",
        description="Desc2",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeBrandRepository(brands=[brand1, brand2])
    fake_uow = FakeUnitOfWork(brand_repository=fake_repo)
    service = BrandServiceImpl(unit_of_work=fake_uow)

    dto = UpdateBrandDTO(id=1, name="Adidas", description="Desc1")

    with pytest.raises(UniqueViolation, match="Brand name should be UNIQUE"):
        await service.update(dto)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_brand_success():
    brand = Brand(
        id=1,
        name="Nike",
        description="Sports brand",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeBrandRepository(brands=[brand])
    fake_uow = FakeUnitOfWork(brand_repository=fake_repo)
    service = BrandServiceImpl(unit_of_work=fake_uow)

    await service.delete(1)

    assert brand.deleted_at is not None
    assert fake_uow.committed is True


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_brand_not_found_raises_entity_not_found(brand_service):
    with pytest.raises(EntityNotFound):
        await brand_service.delete(999)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_all_by_ids_success():
    brand1 = Brand(
        id=1,
        name="Nike",
        description="Desc1",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    brand2 = Brand(
        id=2,
        name="Adidas",
        description="Desc2",
        created_at=datetime.now(),
        updated_at=None,
        deleted_at=None,
    )
    fake_repo = FakeBrandRepository(brands=[brand1, brand2])
    fake_uow = FakeUnitOfWork(brand_repository=fake_repo)
    service = BrandServiceImpl(unit_of_work=fake_uow)

    dto = IdsDTO(ids=[1, 2, 999])
    result = await service.delete_all_by_ids(dto)

    assert result.deleted_ids == [1, 2]
    assert result.not_existed_ids == [999]
    assert brand1.deleted_at is not None
    assert brand2.deleted_at is not None
