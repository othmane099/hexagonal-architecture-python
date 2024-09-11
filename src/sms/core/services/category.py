from datetime import datetime

from dependency_injector.wiring import Provide
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from src.sms.core.domain.dtos import (
    CategoryResponseDTO, CreateCategoryDTO, DeleteAllByIdsResponseDTO, IdsDTO,
    UpdateCategoryDTO, convert_category_to_category_response_dto)
from src.sms.core.domain.models import Category
from src.sms.core.exceptions import UniqueViolation
from src.sms.core.ports.services import CategoryService
from src.sms.core.ports.unit_of_works import CategoryUnitOfWork
from src.sms.helpers import SortDirection, get_existed_entity_by_id


class CategoryServiceImpl(CategoryService):

    def __init__(
        self,
        category_unit_of_work: CategoryUnitOfWork = Provide["category_unit_of_work"],
    ):
        self.category_unit_of_work = category_unit_of_work

    async def create(self, dto: CreateCategoryDTO) -> CategoryResponseDTO:
        async with self.category_unit_of_work as uow:
            category = await uow.repository.find_by_name(dto.name)
            if category:
                raise UniqueViolation("Category name should be UNIQUE")
            category = Category(
                id=None,
                code=dto.code,
                name=dto.name,
                created_at=None,
                updated_at=None,
                deleted_at=None,
            )
            self.category_unit_of_work.repository.create(category)
            await uow.commit()
            return convert_category_to_category_response_dto(category)

    async def delete(self, category_id: int) -> None:
        async with self.category_unit_of_work as uow:
            category = await get_existed_entity_by_id(uow, category_id)
            category.deleted_at = datetime.now()
            await uow.commit()

    async def update(self, dto: UpdateCategoryDTO) -> CategoryResponseDTO:
        async with self.category_unit_of_work as uow:
            category = await get_existed_entity_by_id(uow, dto.id)
            if category.name != dto.name or category.code != dto.code:
                if category.code != dto.code:
                    tmp_category = await uow.repository.find_by_code(dto.code)
                    if tmp_category:
                        raise UniqueViolation("Brand code should be UNIQUE")
                    category.code = dto.code
                if category.name != dto.name:
                    tmp_category = await uow.repository.find_by_name(dto.name)
                    if tmp_category:
                        raise UniqueViolation("Brand name should be UNIQUE")
                    category.name = dto.name
                category.updated_at = datetime.now()
                await uow.commit()
            return convert_category_to_category_response_dto(category)

    async def find_by_id(self, category_id: int) -> CategoryResponseDTO:
        async with self.category_unit_of_work as uow:
            category = await get_existed_entity_by_id(uow, category_id)
            return convert_category_to_category_response_dto(category)

    async def find_all(
        self,
        keyword: str | None,
        page: int,
        size: int,
        sort_column: str,
        sort_dir: SortDirection,
    ) -> Page[CategoryResponseDTO]:
        async with self.category_unit_of_work as uow:
            stmt = uow.repository.get_find_all_stmt(keyword, sort_column, sort_dir)
            return await paginate(
                uow.session,
                stmt,
                transformer=lambda rows: [
                    convert_category_to_category_response_dto(row) for row in rows
                ],
                params=Params(page=page, size=size),
            )

    async def delete_all_by_ids(self, dto: IdsDTO) -> DeleteAllByIdsResponseDTO:
        ids = dto.ids
        async with self.category_unit_of_work as uow:
            categories = await uow.repository.find_all_by_ids(ids)
            categories_ids = [b.id for b in categories]
            not_existed_ids = [id_ for id_ in ids if id_ not in categories_ids]
            for bid in categories_ids:
                category = await uow.repository.find_by_id(bid)
                category.deleted_at = datetime.now()
            await uow.commit()
            return DeleteAllByIdsResponseDTO(
                not_existed_ids=not_existed_ids,
                deleted_ids=categories_ids,
            )
