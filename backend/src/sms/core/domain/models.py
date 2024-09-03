from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class BaseEntityMixin:
    id: int
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None


@dataclass
class Brand(BaseEntityMixin):
    name: str
    description: str | None


@dataclass
class Category(BaseEntityMixin):
    code: str
    name: str


@dataclass
class ProductVariant(BaseEntityMixin):
    product_id: int
    code: str
    name: str
    cost: float
    price: float
    image: str | None
    qty: float


@dataclass
class ProductWarehouse(BaseEntityMixin):
    product_id: int
    warehouse_id: int
    product_variant_id: int | None
    qty: float


class ProductType(str, Enum):
    STANDARD = "standard"
    VARIABLE = "variable"


@dataclass
class Product(BaseEntityMixin):
    category_id: int
    brand_id: int | None
    unit_id: int
    unit_sale_id: int
    unit_purchase_id: int
    type: ProductType
    code: str
    name: str
    cost: float
    price: float
    tax_net: float | None
    tax_method: str
    image: str | None
    description: str | None
    stock_alert: float | None
    has_variant: bool
    is_for_sale: bool
    is_active: bool


@dataclass
class Unit(BaseEntityMixin):
    base_unit_id: int | None
    name: str
    short_name: str
    operator: str | None
    operator_value: str | None


@dataclass
class Warehouse(BaseEntityMixin):
    name: str
    city: str | None
    mobile: str | None
    email: str | None
