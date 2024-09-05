from datetime import datetime

from dependency_injector.wiring import Provide
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from src.sms.core.domain.dtos import (BrandResponseDTO, CreateBrandDTO,
                                      DeleteAllByIdsResponseDTO, IdsDTO,
                                      UpdateBrandDTO,
                                      convert_brand_to_brand_response_dto)
from src.sms.core.domain.models import Brand
from src.sms.core.exceptions import UniqueViolation
from src.sms.core.ports.services import BrandService
from src.sms.core.ports.unit_of_works import BrandUnitOfWork
from src.sms.helpers import SortDirection, get_existed_entity_by_id


class BrandServiceImpl(BrandService):

    def __init__(
        self, brand_unit_of_work: BrandUnitOfWork = Provide["brand_unit_of_work"]
    ):
        self.brand_unit_of_work = brand_unit_of_work

    async def create(self, dto: CreateBrandDTO) -> BrandResponseDTO:
        async with self.brand_unit_of_work as uow:
            brand = await uow.repository.find_by_name(dto.name)
            if brand:
                raise UniqueViolation("Brand name should be UNIQUE")
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

    async def delete(self, brand_id: int) -> None:
        async with self.brand_unit_of_work as uow:
            brand = await get_existed_entity_by_id(uow, brand_id)
            brand.deleted_at = datetime.now()
            await uow.commit()

    async def update(self, dto: UpdateBrandDTO) -> BrandResponseDTO:
        async with self.brand_unit_of_work as uow:
            brand = await get_existed_entity_by_id(uow, dto.id)
            if brand.name != dto.name or brand.description != dto.description:
                if brand.name != dto.name:
                    tmp_brand = await uow.repository.find_by_name(dto.name)
                    if tmp_brand:
                        raise UniqueViolation("Brand name should be UNIQUE")
                    brand.name = dto.name
                if brand.description != dto.description:
                    brand.description = dto.description
                brand.updated_at = datetime.now()
                await uow.commit()
            return convert_brand_to_brand_response_dto(brand)

    async def find_by_id(self, brand_id: int) -> BrandResponseDTO:
        async with self.brand_unit_of_work as uow:
            brand = await get_existed_entity_by_id(uow, brand_id)
            return convert_brand_to_brand_response_dto(brand)

    async def find_all(
        self,
        keyword: str | None,
        page: int,
        size: int,
        sort_column: str,
        sort_dir: SortDirection,
    ) -> Page[BrandResponseDTO]:
        async with self.brand_unit_of_work as uow:
            stmt = uow.repository.get_find_all_stmt(keyword, sort_column, sort_dir)
            return await paginate(
                uow.session,
                stmt,
                transformer=lambda rows: [
                    convert_brand_to_brand_response_dto(row) for row in rows
                ],
                params=Params(page=page, size=size),
            )

    async def delete_all_by_ids(self, dto: IdsDTO) -> DeleteAllByIdsResponseDTO:
        ids = dto.ids
        async with self.brand_unit_of_work as uow:
            brands = await uow.repository.find_all_by_ids(ids)
            brands_ids = [b.id for b in brands]
            not_existed_ids = [id_ for id_ in ids if id_ not in brands_ids]
            for bid in brands_ids:
                brand = await uow.repository.find_by_id(bid)
                brand.deleted_at = datetime.now()
            await uow.commit()
            return DeleteAllByIdsResponseDTO(
                not_existed_ids=not_existed_ids,
                deleted_ids=brands_ids,
            )
