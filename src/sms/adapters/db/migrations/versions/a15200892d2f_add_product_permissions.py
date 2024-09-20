"""add product permissions

Revision ID: a15200892d2f
Revises: c1b9a38f3cff
Create Date: 2024-09-11 14:32:59.544191

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a15200892d2f"
down_revision: Union[str, None] = "c1b9a38f3cff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO permissions (name, label, description, created_at)
        VALUES 
        ('products_view', 'Products View', 'View products', NOW()),
        ('products_add', 'Products Add', 'Add products', NOW()),
        ('products_edit', 'Products Edit', 'Edit products', NOW()),
        ('products_delete', 'Products Delete', 'Delete products', NOW())
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM permissions WHERE name IN ('products_view', 'products_add', 'products_edit', 'products_delete')
        """
    )
