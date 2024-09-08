from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.sms.constants import DATETIME_FORMAT, LOCAL_TIMEZONE
from src.sms.core.domain.models import Brand, User


def convert_datetime_to_str(dt: datetime) -> str | None:
    if dt:
        dt_with_tz = dt.astimezone(LOCAL_TIMEZONE)
        d = dt_with_tz.strftime(DATETIME_FORMAT)
        return d
    return None


class GlobalConfigDictMixin:
    model_config = ConfigDict(extra="forbid")


class IdsDTO(GlobalConfigDictMixin, BaseModel):
    ids: list[int]


class DeleteAllByIdsResponseDTO(GlobalConfigDictMixin, BaseModel):
    not_existed_ids: list[int] | None = None
    existed_not_deleted_ids: list[int] | None = None
    deleted_ids: list[int] | None


class CreateBrandDTO(GlobalConfigDictMixin, BaseModel):
    name: str
    description: str | None = None


class UpdateBrandDTO(GlobalConfigDictMixin, BaseModel):
    id: int
    name: str
    description: str | None = None


class BrandResponseDTO(GlobalConfigDictMixin, BaseModel):
    id: int
    name: str
    description: str | None
    created_at: str
    updated_at: str | None
    deleted_at: str | None


def convert_brand_to_brand_response_dto(brand: Brand) -> BrandResponseDTO:
    return BrandResponseDTO(
        id=brand.id,
        name=brand.name,
        description=brand.description,
        created_at=convert_datetime_to_str(brand.created_at),
        updated_at=convert_datetime_to_str(brand.updated_at),
        deleted_at=convert_datetime_to_str(brand.deleted_at),
    )


# ========== USER ==========


class UserResponseDTO(GlobalConfigDictMixin, BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    phone: str
    is_active: bool
    created_at: str
    updated_at: str | None
    deleted_at: str | None


def convert_user_to_user_response_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        phone=user.phone,
        is_active=user.is_active,
        created_at=convert_datetime_to_str(user.created_at),
        updated_at=convert_datetime_to_str(user.updated_at),
        deleted_at=convert_datetime_to_str(user.deleted_at),
    )
