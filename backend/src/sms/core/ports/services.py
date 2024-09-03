from abc import ABC, abstractmethod

from src.sms.core.domain.dtos import CreateBrandDTO


class BrandService(ABC):
    @abstractmethod
    async def create(self, dto: CreateBrandDTO):
        raise NotImplementedError
