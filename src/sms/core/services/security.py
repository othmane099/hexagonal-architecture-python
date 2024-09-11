from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from src.sms.constants import BRAND_PERMISSION
from src.sms.core.domain.dtos import LoginResponseDTO
from src.sms.core.domain.models import User
from src.sms.core.exceptions import InvalidCredential
from src.sms.core.ports.services import AuthenticationService
from src.sms.core.ports.unit_of_works import RoleUnitOfWork, UserUnitOfWork

SECRET_KEY = "399c72082b3ed6a0956e88619a48c7912e7dc54b95d4a5a1197b0a12cc2951ba"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a password using Bcrypt algorithm"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password, hashed_password):
    """Verify a password against a hashed password"""
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


@inject
async def has_permission(
    role_name: str,
    permission_name: str,
    role_unit_of_work: RoleUnitOfWork = Provide["role_unit_of_work"],
) -> bool:
    async with role_unit_of_work as uow:
        return await uow.repository.role_has_permission(role_name, permission_name)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Validates token and returns User"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredential("Could not validate credentials")
    except InvalidTokenError:
        raise InvalidCredential("Could not validate credentials")
    user = await load_user_by_username(username=username)
    if user is None:
        raise InvalidCredential("Could not validate credentials")
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Verifies current User if it is active"""
    if not current_user.is_active:
        raise InvalidCredential("User is not active")
    return current_user


def verify_role(
    required_role: str, enabled_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Verifies current User Role"""
    if required_role not in enabled_user.role.name:
        raise InvalidCredential("Role is not allowed")
    return enabled_user


async def has_brand_permission(
    enabled_user: Annotated[User, Depends(get_current_active_user)]
) -> bool:
    """Verifies if the current user's role has brand permission."""
    return await has_permission(enabled_user.role.name, BRAND_PERMISSION)


async def has_category_permission(
    enabled_user: Annotated[User, Depends(get_current_active_user)]
) -> bool:
    """Verifies if the current user's role has category permission."""
    return await has_permission(enabled_user.role.name, BRAND_PERMISSION)


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
            "role": user.role.name,
        }
        access_token = create_access_token(payload)
        return LoginResponseDTO(access_token=access_token)
