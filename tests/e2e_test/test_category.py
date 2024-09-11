import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from src.sms.adapters.entry_points.api.app import app
from src.sms.core.domain.dtos import (CreateCategoryDTO, IdsDTO,
                                      UpdateCategoryDTO)
from src.sms.helpers import SortDirection

client = TestClient(app)


@pytest.mark.asyncio(loop_scope="session")
async def test_create(get_user_service_impl):
    dto = CreateCategoryDTO(name="e2e_category_name", code="e2e_category_code")
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/api/v1/categories",
            json=CreateCategoryDTO.model_dump(dto),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["id"] is not None
        assert response.json()["data"]["name"] == dto.name
        assert response.json()["data"]["code"] == dto.code
        assert response.json()["data"]["created_at"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_update(get_category_service_impl, get_user_service_impl):
    categories = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    existed_category = categories.items[0]
    print(existed_category)
    dto = UpdateCategoryDTO(
        id=existed_category.id,
        name="updated_e2e_category_name",
        code=existed_category.code,
    )
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.put(
            "/api/v1/categories",
            json=UpdateCategoryDTO.model_dump(dto),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["id"] == dto.id
        assert response.json()["data"]["name"] == dto.name
        assert response.json()["data"]["code"] == dto.code
        assert response.json()["data"]["created_at"] is not None
        assert response.json()["data"]["updated_at"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories(get_category_service_impl, get_user_service_impl):
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]

    categories = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories?page=1&size=10",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == len(categories.items)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_sorting_and_direction(
    get_category_service_impl, get_user_service_impl
):
    dto = CreateCategoryDTO(name="one_more_category", code="one_more_category_code")
    await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(name="one_more_category1", code="one_more_category_code1")
    await get_category_service_impl.create(dto)

    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories?page=1&size=10&sort_column=id&sort_dir=asc",
            headers={"Authorization": f"Bearer {access_token}"},
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
            "/api/v1/categories?page=1&size=10&sort_column=id&sort_dir=desc",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        items = response.json()["items"]
        first_item = items[0]
        last_item = items[-1]
        assert response.status_code == 200
        assert first_item.get("id") > last_item.get("id")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories__search_by_keyword(
    get_category_service_impl, get_user_service_impl
):
    dto = CreateCategoryDTO(name="other_category", code="other_category_code")
    b1 = await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(name="other_category1", code="other_category1_code")
    b2 = await get_category_service_impl.create(dto)
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
    # Search by keyword = other_category
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories?page=1&size=10&keyword=other_category",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
    # Search by not existed keyword
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories?page=1&size=10&keyword=random",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 0
    # Search by code keyword
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories?page=1&size=10&keyword=other_category_code",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1
    # Search by name keyword
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories?page=1&size=10&keyword=other_category1",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category(get_category_service_impl, get_user_service_impl):
    category = await get_category_service_impl.find_by_id(1)
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.get(
            "/api/v1/categories/1",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["id"] == category.id
        assert response.json()["data"]["name"] == category.name
        assert response.json()["data"]["code"] == category.code
        assert response.json()["data"]["created_at"] == category.created_at


@pytest.mark.asyncio(loop_scope="session")
async def test_delete(get_category_service_impl, get_user_service_impl):
    existed_category_before_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.delete(
            "/api/v1/categories/1",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["detail"] == "Category deleted successfully"

    existed_category_after_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_category_after_delete.items)
        == len(existed_category_before_delete.items) - 1
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_all_by_ids(get_category_service_impl, get_user_service_impl):
    dto = CreateCategoryDTO(
        name="test_delete_all_by_ids", code="test_delete_all_by_ids_code"
    )
    b1 = await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(
        name="test_delete_all_by_ids1", code="test_delete_all_by_ids_code1"
    )
    b2 = await get_category_service_impl.create(dto)
    dto = CreateCategoryDTO(
        name="test_delete_all_by_ids2", code="test_delete_all_by_ids_code2"
    )
    b3 = await get_category_service_impl.create(dto)
    ids = [b1.id, b2.id, b3.id, 999]
    dto = IdsDTO(ids=ids)
    existed_category_before_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    test_owner = await get_user_service_impl.find_by_username("test_owner")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": test_owner.username, "password": "123456"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/api/v1/categories/delete-all-by-ids",
            json=IdsDTO.model_dump(dto),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["not_existed_ids"] == [999]
        assert response.json()["data"]["deleted_ids"] == [b1.id, b2.id, b3.id]

    existed_category_after_delete = await get_category_service_impl.find_all(
        keyword=None, page=1, size=10, sort_column="name", sort_dir=SortDirection.ASC
    )
    assert (
        len(existed_category_after_delete.items)
        == len(existed_category_before_delete.items) - 3
    )
