from datetime import datetime

from src.sms.core.domain.models import Brand
from src.sms.core.ports.repositories import BrandRepository


class FakeBrandRepository(BrandRepository):

    def __init__(self, brands: list[Brand] | None = None):
        self._brands: list[Brand] = brands if brands is not None else []
        self._id_counter = 1

    def create(self, brand: Brand) -> None:
        if brand.id is None:
            brand.id = self._id_counter
            self._id_counter += 1
        if brand.created_at is None:
            brand.created_at = datetime.now()
        self._brands.append(brand)

    async def find_by_id(self, id_: int) -> Brand | None:
        for brand in self._brands:
            if brand.id == id_ and brand.deleted_at is None:
                return brand
        return None

    async def find_by_name(self, name: str) -> Brand | None:
        for brand in self._brands:
            if brand.name == name and brand.deleted_at is None:
                return brand
        return None

    async def find_all_by_ids(self, ids: list[int]) -> list[Brand]:
        return [
            brand
            for brand in self._brands
            if brand.id in ids and brand.deleted_at is None
        ]
