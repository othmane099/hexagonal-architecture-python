import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_find_user_by_username(get_user_service_impl, init_owner):
    user = await get_user_service_impl.find_by_username("test_owner")
    assert user.id is not None
    assert user.username == "test_owner"
    assert user.created_at is not None
