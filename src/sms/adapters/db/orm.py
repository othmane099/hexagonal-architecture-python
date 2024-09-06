from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text, func)
from sqlalchemy.orm import registry, relationship

from src.sms.core.domain.models import (Brand, Category, Permission, Product,
                                        ProductType, ProductVariant, Role,
                                        User)

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
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)

category = Table(
    "categories",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("code", String, nullable=False, unique=True),
    Column("name", String, nullable=False, unique=True),
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
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
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
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
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)

permission = Table(
    "permissions",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("name", String, nullable=False, unique=True),
    Column("label", String, nullable=False, unique=True),
    Column("description", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)

role = Table(
    "roles",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("name", String, nullable=False, unique=True),
    Column("label", String, nullable=False, unique=True),
    Column("description", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)

user = Table(
    "users",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    ),
    Column("firstname", String, nullable=False),
    Column("lastname", String, nullable=False),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("phone", String, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)

# ==== Many to many ====

role_permission_association = Table(
    "roles_permissions",
    mapper_registry.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

user_role_association = Table(
    "users_roles",
    mapper_registry.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
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
    mapper_registry.map_imperatively(
        Permission,
        permission,
        properties={
            "roles": relationship(
                "Role",
                secondary=role_permission_association,
                back_populates="permissions",
            ),
        },
    )
    mapper_registry.map_imperatively(
        Role,
        role,
        properties={
            "permissions": relationship(
                "Permission",
                secondary=role_permission_association,
                back_populates="roles",
            ),
            "users": relationship(
                "User", secondary=user_role_association, back_populates="roles"
            ),
        },
    )
    mapper_registry.map_imperatively(
        User,
        user,
        properties={
            "roles": relationship(
                "Role", secondary=user_role_association, back_populates="users"
            ),
        },
    )
