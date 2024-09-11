"""add category permission

Revision ID: d93dee229fbb
Revises: 784e6109e7ed
Create Date: 2024-09-11 12:56:27.779153

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d93dee229fbb"
down_revision: Union[str, None] = "784e6109e7ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO permissions (name, label, description, created_at)
        VALUES ('category', 'Category', 'Category crud permissions', NOW())
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM permissions WHERE name = 'category'
        """
    )
