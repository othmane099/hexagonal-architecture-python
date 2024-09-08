from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dependency_injector.wiring import Provide, inject
from fastapi.security import OAuth2PasswordRequestForm

from src.sms.core.domain.dtos import LoginResponseDTO
from src.sms.core.domain.models import User
from src.sms.core.exceptions import InvalidCredential
from src.sms.core.ports.services import AuthenticationService
from src.sms.core.ports.unit_of_works import UserUnitOfWork

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a password using Bcrypt algorithm"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password, hashed_password):
    """Verify a password against a hashed password"""
    print(plain_password)
    print(hashed_password)
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict):
    """Creates a JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@inject
async def load_user_by_username(
    username: str, user_unit_of_work: UserUnitOfWork = Provide["user_unit_of_work"]
) -> User | None:
    async with user_unit_of_work as uow:
        return await uow.repository.find_by_username(username)


class AuthenticationServiceImpl(AuthenticationService):

    async def authenticate(
        self, form_data: OAuth2PasswordRequestForm
    ) -> LoginResponseDTO:
        user = await load_user_by_username(form_data.username)
        if not user:
            raise InvalidCredential("Incorrect username or password")
        if not verify_password(form_data.password, user.password):
            raise InvalidCredential("Incorrect username or password")
        payload = {
            "sub": user.username,
        }
        access_token = create_access_token(payload)
        return LoginResponseDTO(access_token=access_token)
