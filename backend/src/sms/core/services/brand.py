from datetime import datetime

from dependency_injector.wiring import Provide

from src.sms.core.domain.dtos import (CreateBrandDTO,
                                      convert_brand_to_brand_response_dto)
from src.sms.core.domain.models import Brand
from src.sms.core.ports.services import BrandService
from src.sms.core.ports.unit_of_works import BrandUnitOfWork


class BrandServiceImpl(BrandService):

    def __init__(
        self, brand_unit_of_work: BrandUnitOfWork = Provide["brand_unit_of_work"]
    ):
        self.brand_unit_of_work = brand_unit_of_work

    async def create(self, dto: CreateBrandDTO):
        async with self.brand_unit_of_work as uow:
            brand = Brand(
                id=None,
                name=dto.name,
                description=dto.description,
                created_at=datetime.now(),
                updated_at=None,
                deleted_at=None,
            )
            self.brand_unit_of_work.repository.create(brand)
            await uow.commit()
            return convert_brand_to_brand_response_dto(brand)
