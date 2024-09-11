"""Assign category permission to owner role

Revision ID: c1b9a38f3cff
Revises: d93dee229fbb
Create Date: 2024-09-11 12:58:10.782276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1b9a38f3cff'
down_revision: Union[str, None] = 'd93dee229fbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles, permissions
        WHERE roles.name = 'owner' AND permissions.name = 'category'
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM roles_permissions
        WHERE role_id = (SELECT id FROM roles WHERE name = 'owner')
        AND permission_id = (SELECT id FROM permissions WHERE name = 'category')
        """
    )
