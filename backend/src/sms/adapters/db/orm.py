from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text)
from sqlalchemy.orm import registry, relationship

from src.sms.core.domain.models import (Brand, Category, Product, ProductType,
                                        ProductVariant, ProductWarehouse, Unit,
                                        Warehouse)

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

unit = Table(
    "units",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("base_unit_id", Integer, ForeignKey("units.id"), nullable=True),
    Column("name", String, nullable=False, unique=True),
    Column("short_name", String, nullable=False, unique=True),
    Column("operator", String, nullable=True),
    Column("operator_value", String, nullable=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=True),
    Column("deleted_at", DateTime, nullable=True),
)

warehouse = Table(
    "warehouses",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("name", String, nullable=False, unique=True),
    Column("city", String, nullable=True),
    Column("mobile", String, nullable=True),
    Column("email", String, nullable=True),
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
    Column("unit_id", Integer, ForeignKey("units.id"), nullable=False),
    Column("unit_sale_id", Integer, ForeignKey("units.id"), nullable=False),
    Column("unit_purchase_id", Integer, ForeignKey("units.id"), nullable=False),
    Column("type", Enum(ProductType), nullable=False),
    Column("code", String, nullable=False),
    Column("name", String, nullable=False),
    Column("cost", Float, nullable=False),
    Column("price", Float, nullable=False),
    Column("tax_net", Float, nullable=True),
    Column("tax_method", String, nullable=False),
    Column("image", String, nullable=True),
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

product_warehouse = Table(
    "product_warehouses",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("warehouse_id", Integer, ForeignKey("warehouses.id"), nullable=False),
    Column(
        "product_variant_id", Integer, ForeignKey("product_variants.id"), nullable=True
    ),
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
        Unit,
        unit,
        properties={
            "products": relationship("Product", back_populates="unit"),
        },
    )
    mapper_registry.map_imperatively(
        Warehouse,
        warehouse,
        properties={
            "products": relationship("ProductWarehouse", back_populates="warehouse"),
            "product_variants": relationship(
                "ProductWarehouse", back_populates="warehouse"
            ),
        },
    )
    mapper_registry.map_imperatively(
        Product,
        product,
        properties={
            "brand": relationship("Brand", back_populates="products"),
            "category": relationship("Category", back_populates="products"),
            "unit": relationship("Unit", back_populates="products"),
            "variants": relationship("ProductVariant", back_populates="product"),
            "warehouses": relationship("ProductWarehouse", back_populates="product"),
        },
    )
    mapper_registry.map_imperatively(
        ProductVariant,
        product_variant,
        properties={
            "product": relationship("Product", back_populates="variants"),
            "warehouses": relationship(
                "ProductWarehouse", back_populates="product_variant"
            ),
        },
    )
    mapper_registry.map_imperatively(
        ProductWarehouse,
        product_warehouse,
        properties={
            "product": relationship("Product", back_populates="warehouses"),
            "warehouse": relationship("Warehouse", back_populates="products"),
            "product_variant": relationship(
                "ProductVariant", back_populates="warehouses"
            ),
        },
    )
