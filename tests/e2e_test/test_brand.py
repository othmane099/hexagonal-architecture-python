import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from src.sms.adapters.entry_points.api.app import app
from src.sms.core.domain.dtos import CreateBrandDTO, IdsDTO, UpdateBrandDTO
from src.sms.helpers import SortDirection

client = TestClient(app)


@pytest.mark.asyncio(loop_scope="session")
async def test_create(drop_and_create_database):
    dto = CreateBrandDTO(name="e2e_brand_name", description="e2e_brand_description")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post("/api/v1/brands", json=CreateBrandDTO.model_dump(dto))
        assert response.status_code == 200
        assert response.json()["data"]["id"] is not None
        assert response.json()["data"]["name"] == dto.name
        assert response.json()["data"]["description"] == dto.description
        assert response.json()["data"]["created_at"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_update(get_brand_service_impl):
    brands = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    existed_brand = brands.items[0]
    dto = UpdateBrandDTO(
        id=existed_brand.id,
        name="updated_e2e_brand_name",
        description=existed_brand.description,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.put("/api/v1/brands", json=UpdateBrandDTO.model_dump(dto))
        assert response.status_code == 200
        assert response.json()["data"]["id"] == dto.id
        assert response.json()["data"]["name"] == dto.name
        assert response.json()["data"]["description"] == dto.description
        assert response.json()["data"]["created_at"] is not None
        assert response.json()["data"]["updated_at"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_brands(get_brand_service_impl):
    brands = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get("/api/v1/brands?page=1&size=10")
        assert response.status_code == 200
        assert len(response.json()["items"]) == len(brands.items)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_brands_sorting_and_direction(get_brand_service_impl):
    dto = CreateBrandDTO(name="one_more_brand", description=None)
    await get_brand_service_impl.create(dto)
    dto = CreateBrandDTO(name="one_more_brand1", description=None)
    await get_brand_service_impl.create(dto)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/brands?page=1&size=10&sort_column=id&sort_dir=asc"
        )
        items = response.json()["items"]
        first_item = items[0]
        last_item = items[-1]
        assert response.status_code == 200
        assert first_item.get("id") < last_item.get("id")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/brands?page=1&size=10&sort_column=id&sort_dir=desc"
        )
        items = response.json()["items"]
        first_item = items[0]
        last_item = items[-1]
        assert response.status_code == 200
        assert first_item.get("id") > last_item.get("id")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_brands__search_by_keyword(get_brand_service_impl):
    dto = CreateBrandDTO(name="other_brand", description=None)
    b1 = await get_brand_service_impl.create(dto)
    dto = CreateBrandDTO(name="other_brand1", description="other_brand_description")
    b2 = await get_brand_service_impl.create(dto)
    # Search by keyword = other_brand
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get("/api/v1/brands?page=1&size=10&keyword=other_brand")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
    # Search by not existed keyword
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get("/api/v1/brands?page=1&size=10&keyword=random")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 0
    # Search by description keyword
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/brands?page=1&size=10&keyword=other_brand_description"
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1
    # Search by name keyword
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get("/api/v1/brands?page=1&size=10&keyword=other_brand1")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_brand(get_brand_service_impl):
    brand = await get_brand_service_impl.find_by_id(1)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get("/api/v1/brands/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == brand.id
        assert response.json()["data"]["name"] == brand.name
        assert response.json()["data"]["description"] == brand.description
        assert response.json()["data"]["created_at"] == brand.created_at


@pytest.mark.asyncio(loop_scope="session")
async def test_delete(get_brand_service_impl):
    existed_brand_before_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.delete("/api/v1/brands/1")
        assert response.status_code == 200
        assert response.json()["detail"] == "Brand deleted successfully"

    existed_brand_after_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_brand_after_delete.items)
        == len(existed_brand_before_delete.items) - 1
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
    existed_brand_before_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/api/v1/brands/delete-all-by-ids", json=IdsDTO.model_dump(dto)
        )
        assert response.status_code == 200
        assert response.json()["data"]["not_existed_ids"] == [999]
        assert response.json()["data"]["deleted_ids"] == [b1.id, b2.id, b3.id]

    existed_brand_after_delete = await get_brand_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_brand_after_delete.items)
        == len(existed_brand_before_delete.items) - 3
    )
