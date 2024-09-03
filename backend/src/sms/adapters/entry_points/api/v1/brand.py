import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination import Page

from src.sms.core.domain.dtos import (BrandResponseDTO, CreateBrandDTO,
                                      UpdateBrandDTO)
from src.sms.core.exceptions import EntityNotFound, UniqueViolation
from src.sms.core.ports.services import BrandService

router = APIRouter()


@router.get("", response_model=Page[BrandResponseDTO])
@inject
async def get_brands(
    page: int = 1,
    size: int = 20,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Page[BrandResponseDTO]:
    response = await brand_service_impl.find_all(page, size)
    return response


@router.get("/{brand_id}", response_model=None)
@inject
async def get_brand(
    brand_id: int,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        response = await brand_service_impl.find_by_id(brand_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(
        content=json.dumps({"data": BrandResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.post("", response_model=None)
@inject
async def create(
    dto: CreateBrandDTO,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        response = await brand_service_impl.create(dto)
    except UniqueViolation as e:
        raise HTTPException(status_code=409, detail=e.message)
    return Response(
        content=json.dumps({"data": BrandResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.put("", response_model=None)
@inject
async def update(
    dto: UpdateBrandDTO,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        response = await brand_service_impl.update(dto)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except UniqueViolation as e:
        raise HTTPException(status_code=409, detail=e.message)
    return Response(
        content=json.dumps({"data": BrandResponseDTO.model_dump(response)}),
        media_type="application/json",
        status_code=200,
    )


@router.delete("/{brand_id}", response_model=None)
@inject
async def delete(
    brand_id: int,
    brand_service_impl: BrandService = Depends(Provide["brand_service_impl"]),
) -> Response:
    try:
        await brand_service_impl.delete(brand_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return Response(
        content=json.dumps({"detail": "Brand deleted successfully"}),
        media_type="application/json",
        status_code=200,
    )
