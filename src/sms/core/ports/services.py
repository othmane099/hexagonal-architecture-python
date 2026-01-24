from typing import Protocol

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page

from src.sms.core.domain.dtos import (BrandResponseDTO, CategoryResponseDTO,
                                      CreateBrandDTO, CreateCategoryDTO,
                                      DeleteAllByIdsResponseDTO, IdsDTO,
                                      LoginResponseDTO, UpdateBrandDTO,
                                      UpdateCategoryDTO, UserResponseDTO)
from src.sms.helpers import SortDirection


class BrandService(Protocol):
    async def create(self, dto: CreateBrandDTO) -> BrandResponseDTO: ...

    async def delete(self, brand_id: int) -> None: ...

    async def update(self, dto: UpdateBrandDTO) -> BrandResponseDTO: ...

    async def find_by_id(self, brand_id: int) -> BrandResponseDTO: ...

    async def find_all(
        self,
        keyword: str | None,
        page: int,
        size: int,
        sort_column: str,
        sort_dir: SortDirection,
    ) -> Page[BrandResponseDTO]: ...

    async def delete_all_by_ids(self, dto: IdsDTO) -> DeleteAllByIdsResponseDTO: ...


class UserService(Protocol):

    async def find_by_username(self, username: str) -> UserResponseDTO: ...


class AuthenticationService(Protocol):

    async def authenticate(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> LoginResponseDTO: ...


class CategoryService(Protocol):
    async def create(self, dto: CreateCategoryDTO) -> CategoryResponseDTO: ...

    async def delete(self, category_id: int) -> None: ...

    async def update(self, dto: UpdateCategoryDTO) -> CategoryResponseDTO: ...

    async def find_by_id(self, category_id: int) -> CategoryResponseDTO: ...

    async def find_all(
        self,
        keyword: str | None,
        page: int,
        size: int,
        sort_column: str,
        sort_dir: SortDirection,
    ) -> Page[CategoryResponseDTO]: ...

    async def delete_all_by_ids(self, dto: IdsDTO) -> DeleteAllByIdsResponseDTO: ...
