from abc import ABC, abstractmethod

from fastapi_pagination import Page

from src.sms.core.domain.dtos import CreateBrandDTO, BrandResponseDTO, UpdateBrandDTO


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
    async def find_all(self, page: int, size: int) -> Page[BrandResponseDTO]:
        raise NotImplementedError
