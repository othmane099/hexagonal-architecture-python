from datetime import datetime, timezone

import jwt
import pytest
from fastapi.security import OAuth2PasswordRequestForm

from src.sms.core.domain.dtos import LoginResponseDTO
from src.sms.core.exceptions import InvalidCredential
from src.sms.core.ports.unit_of_works import UserUnitOfWork
from src.sms.core.services.security import (ALGORITHM, SECRET_KEY,
                                            AuthenticationServiceImpl,
                                            create_access_token, hash_password,
                                            verify_password)


def test_hash_password():
    password = "mysecretpassword"
    hashed_password = hash_password(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_verify_password():
    password = "mysecretpassword"
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "testuser"
    assert "exp" in decoded_data
    assert datetime.fromtimestamp(decoded_data["exp"], timezone.utc) > datetime.now(
        timezone.utc
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_authenticate_success(mocker):
    mock_user = mocker.Mock()
    mock_user.username = "testuser"
    mock_user.password = hash_password("testpassword")
    mock_repository = mocker.AsyncMock()
    mock_repository.find_by_username.return_value = mock_user
    mock_uow = mocker.Mock(spec=UserUnitOfWork)
    mock_uow.repository = mock_repository
    mocker.patch(
        "src.sms.core.services.security.load_user_by_username", return_value=mock_user
    )

    auth_service = AuthenticationServiceImpl()
    form_data = OAuth2PasswordRequestForm(username="testuser", password="testpassword")

    result = await auth_service.authenticate(form_data)

    assert isinstance(result, LoginResponseDTO)
    assert result.access_token is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_authenticate_invalid_credentials(mocker):
    mock_repository = mocker.AsyncMock()
    mock_repository.find_by_username.return_value = None
    mock_uow = mocker.Mock(spec=UserUnitOfWork)
    mock_uow.repository = mock_repository
    mocker.patch(
        "src.sms.core.services.security.load_user_by_username", return_value=None
    )

    auth_service = AuthenticationServiceImpl()
    form_data = OAuth2PasswordRequestForm(
        username="wronguser", password="wrongpassword"
    )

    with pytest.raises(InvalidCredential):
        await auth_service.authenticate(form_data)
