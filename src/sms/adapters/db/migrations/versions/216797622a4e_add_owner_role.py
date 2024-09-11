"""add owner role

Revision ID: 216797622a4e
Revises: 62b1cbc194b8
Create Date: 2024-09-11 10:38:31.587535

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "216797622a4e"
down_revision: Union[str, None] = "62b1cbc194b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO roles (name, label, description, created_at)
        VALUES ('owner', 'Owner', 'Owner role with full permissions', NOW())
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM roles WHERE name = 'owner'
        """
    )
