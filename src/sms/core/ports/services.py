from abc import ABC, abstractmethod

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page

from src.sms.core.domain.dtos import (BrandResponseDTO, CreateBrandDTO,
                                      DeleteAllByIdsResponseDTO, IdsDTO,
                                      LoginResponseDTO, UpdateBrandDTO,
                                      UserResponseDTO)
from src.sms.helpers import SortDirection


class BrandService(ABC):
    @abstractmethod
    async def create(self, dto: CreateBrandDTO) -> BrandResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, brand_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, dto: UpdateBrandDTO) -> BrandResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, brand_id: int) -> BrandResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        keyword: str | None,
        page: int,
        size: int,
        sort_column: str,
        sort_dir: SortDirection,
    ) -> Page[BrandResponseDTO]:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_by_ids(self, dto: IdsDTO) -> DeleteAllByIdsResponseDTO:
        raise NotImplementedError


class UserService(ABC):

    @abstractmethod
    async def find_by_username(self, username: str) -> UserResponseDTO:
        raise NotImplementedError


class AuthenticationService(ABC):

    @abstractmethod
    async def authenticate(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> LoginResponseDTO:
        raise NotImplementedError
