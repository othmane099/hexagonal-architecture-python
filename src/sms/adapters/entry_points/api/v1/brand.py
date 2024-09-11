import json
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination import Page

from src.sms.core.domain.dtos import (BrandResponseDTO, CreateBrandDTO,
                                      DeleteAllByIdsResponseDTO, IdsDTO,
                                      UpdateBrandDTO)
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.core.ports.services import BrandService
from src.sms.core.services.security import has_brand_permission
from src.sms.helpers import SortDirection

router = APIRouter()


@router.get("", response_model=Page[BrandResponseDTO])
@inject
async def get_brands(
    _: Annotated[bool, Depends(has_brand_permission)],
    keyword: str | None = None,
    page: int = 1,
    size: int = 20,
    sort_column: str = "name",
    sort_dir: SortDirection = SortDirection.ASC,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Page[BrandResponseDTO]:
    response = await brand_service_impl.find_all(
        keyword, page, size, sort_column, sort_dir
    )
    return response


@router.get("/{brand_id}", response_model=None)
@inject
async def get_brand(
    _: Annotated[bool, Depends(has_brand_permission)],
    brand_id: int,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        response = await brand_service_impl.find_by_id(brand_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(
        content=json.dumps({"data": BrandResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.post("", response_model=None)
@inject
async def create(
    _: Annotated[bool, Depends(has_brand_permission)],
    dto: CreateBrandDTO,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        response = await brand_service_impl.create(dto)
    except UniqueViolation as e:
        raise HTTPException(status_code=409, detail=str(e))
    return Response(
        content=json.dumps({"data": BrandResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.put("", response_model=None)
@inject
async def update(
    _: Annotated[bool, Depends(has_brand_permission)],
    dto: UpdateBrandDTO,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        response = await brand_service_impl.update(dto)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UniqueViolation as e:
        raise HTTPException(status_code=409, detail=str(e))
    return Response(
        content=json.dumps({"data": BrandResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.delete("/{brand_id}", response_model=None)
@inject
async def delete(
    _: Annotated[bool, Depends(has_brand_permission)],
    brand_id: int,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        await brand_service_impl.delete(brand_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(
        content=json.dumps({"detail": "Brand deleted successfully"}),
        media_type="application/json",
        status_code=200,
    )


@router.post("/delete-all-by-ids", response_model=None)
@inject
async def delete_all_by_ids(
    _: Annotated[bool, Depends(has_brand_permission)],
    dto: IdsDTO,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    response = await brand_service_impl.delete_all_by_ids(dto)
    return Response(
        content=json.dumps({"data": DeleteAllByIdsResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )
