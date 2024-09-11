"""add brand permission

Revision ID: 62b1cbc194b8
Revises: 40ca2211a7e5
Create Date: 2024-09-11 10:31:33.849247

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "62b1cbc194b8"
down_revision: Union[str, None] = "40ca2211a7e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO permissions (name, label, description, created_at)
        VALUES ('brand', 'Brand', 'Brand crud permissions', NOW())
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM permissions WHERE name = 'brand'
        """
    )
