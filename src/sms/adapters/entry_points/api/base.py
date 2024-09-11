from fastapi import APIRouter

from . import main
from .v1 import brand

api_router = APIRouter()


api_router.include_router(brand.router, prefix="/api/v1/brands", tags=["Brand"])

api_router.include_router(main.router)
