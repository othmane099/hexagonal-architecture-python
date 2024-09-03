from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text)
from sqlalchemy.orm import registry, relationship

from src.sms.core.domain.models import (Brand, Category, Product, ProductType,
                                        ProductVariant)

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

brand = Table(
    "brands",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("name", String, nullable=False),
    Column("description", Text, nullable=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=True),
    Column("deleted_at", DateTime, nullable=True),
)

category = Table(
    "categories",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("code", String, nullable=False, unique=True),
    Column("name", String, nullable=False, unique=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=True),
    Column("deleted_at", DateTime, nullable=True),
)


product = Table(
    "products",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
    Column("brand_id", Integer, ForeignKey("brands.id"), nullable=True),
    Column("type", Enum(ProductType), nullable=False),
    Column("code", String, nullable=False),
    Column("name", String, nullable=False),
    Column("cost", Float, nullable=False),
    Column("price", Float, nullable=False),
    Column("tax_net", Float, nullable=True),
    Column("tax_method", String, nullable=False),
    Column("image", String, nullable=True),
    Column("qty", Float, nullable=False),
    Column("description", Text, nullable=True),
    Column("stock_alert", Float, nullable=True),
    Column("has_variant", Boolean, nullable=False),
    Column("is_for_sale", Boolean, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=True),
    Column("deleted_at", DateTime, nullable=True),
)

product_variant = Table(
    "product_variants",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("cost", Float, nullable=False),
    Column("price", Float, nullable=False),
    Column("code", String, nullable=False),
    Column("image", String, nullable=True),
    Column("qty", Float, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=True),
    Column("deleted_at", DateTime, nullable=True),
)


def start_mappers():
    mapper_registry.map_imperatively(
        Brand,
        brand,
        properties={
            "products": relationship("Product", back_populates="brand"),
        },
    )
    mapper_registry.map_imperatively(
        Category,
        category,
        properties={
            "products": relationship("Product", back_populates="category"),
        },
    )
    mapper_registry.map_imperatively(
        Product,
        product,
        properties={
            "brand": relationship("Brand", back_populates="products"),
            "category": relationship("Category", back_populates="products"),
            "variants": relationship("ProductVariant", back_populates="product"),
        },
    )
    mapper_registry.map_imperatively(
        ProductVariant,
        product_variant,
        properties={
            "product": relationship("Product", back_populates="variants"),
        },
    )
