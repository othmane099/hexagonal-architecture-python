import jwt
import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from src.sms.adapters.entry_points.api.app import app
from src.sms.core.services.security import ALGORITHM, SECRET_KEY

client = TestClient(app)


@pytest.mark.asyncio(loop_scope="session")
async def test_login(init_owner):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as ac:
        response = await ac.post(
            "/token", data={"username": "test_owner", "password": "123456"}
        )
        assert response.status_code == 200
        response_json = response.json()
        decoded_data = jwt.decode(
            response_json["access_token"], SECRET_KEY, algorithms=[ALGORITHM]
        )
        assert decoded_data["sub"] == "test_owner"
