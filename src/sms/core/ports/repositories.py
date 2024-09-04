from abc import ABC, abstractmethod

from sqlalchemy import Select

from src.sms.core.domain.models import Brand


class BrandRepository(ABC):
    @abstractmethod
    def create(self, brand: Brand) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id_: int) -> Brand | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_name(self, name: str) -> Brand | None:
        raise NotImplementedError

    @abstractmethod
    def get_find_all_stmt(self) -> Select[tuple[Brand]]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_ids(self, ids: list[int]) -> list[Brand]:
        raise NotImplementedError
