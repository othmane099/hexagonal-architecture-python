import json
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination import Page

from src.sms.core.domain.dtos import (CategoryResponseDTO, CreateCategoryDTO,
                                      DeleteAllByIdsResponseDTO, IdsDTO,
                                      UpdateCategoryDTO)
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.core.ports.services import CategoryService
from src.sms.core.services.security import has_category_permission
from src.sms.helpers import SortDirection

router = APIRouter()


@router.get("", response_model=Page[CategoryResponseDTO])
@inject
async def get_categories(
    _: Annotated[bool, Depends(has_category_permission)],
    keyword: str | None = None,
    page: int = 1,
    size: int = 20,
    sort_column: str = "name",
    sort_dir: SortDirection = SortDirection.ASC,
    category_service_impl: CategoryService = Depends(Provide["category_service_impl"]),
) -> Page[CategoryResponseDTO]:
    response = await category_service_impl.find_all(
        keyword, page, size, sort_column, sort_dir
    )
    return response


@router.get("/{category_id}", response_model=None)
@inject
async def get_category(
    _: Annotated[bool, Depends(has_category_permission)],
    category_id: int,
    category_service_impl: CategoryService = Depends(Provide["category_service_impl"]),
) -> Response:
    try:
        response = await category_service_impl.find_by_id(category_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(
        content=json.dumps({"data": CategoryResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.post("", response_model=None)
@inject
async def create(
    _: Annotated[bool, Depends(has_category_permission)],
    dto: CreateCategoryDTO,
    category_service_impl: CategoryService = Depends(Provide["category_service_impl"]),
) -> Response:
    try:
        response = await category_service_impl.create(dto)
    except UniqueViolation as e:
        raise HTTPException(status_code=409, detail=str(e))
    return Response(
        content=json.dumps({"data": CategoryResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.put("", response_model=None)
@inject
async def update(
    _: Annotated[bool, Depends(has_category_permission)],
    dto: UpdateCategoryDTO,
    category_service_impl: CategoryService = Depends(Provide["category_service_impl"]),
) -> Response:
    try:
        response = await category_service_impl.update(dto)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UniqueViolation as e:
        raise HTTPException(status_code=409, detail=str(e))
    return Response(
        content=json.dumps({"data": CategoryResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.delete("/{category_id}", response_model=None)
@inject
async def delete(
    _: Annotated[bool, Depends(has_category_permission)],
    category_id: int,
    category_service_impl: CategoryService = Depends(Provide["category_service_impl"]),
) -> Response:
    try:
        await category_service_impl.delete(category_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(
        content=json.dumps({"detail": "Category deleted successfully"}),
        media_type="application/json",
        status_code=200,
    )


@router.post("/delete-all-by-ids", response_model=None)
@inject
async def delete_all_by_ids(
    _: Annotated[bool, Depends(has_category_permission)],
    dto: IdsDTO,
    category_service_impl: CategoryService = Depends(Provide["category_service_impl"]),
) -> Response:
    response = await category_service_impl.delete_all_by_ids(dto)
    return Response(
        content=json.dumps({"data": DeleteAllByIdsResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )
