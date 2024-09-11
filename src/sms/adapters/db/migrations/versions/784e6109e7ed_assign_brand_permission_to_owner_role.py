"""Assign brand permission to owner role

Revision ID: 784e6109e7ed
Revises: 216797622a4e
Create Date: 2024-09-11 10:41:41.082499

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "784e6109e7ed"
down_revision: Union[str, None] = "216797622a4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles, permissions
        WHERE roles.name = 'owner' AND permissions.name = 'brand'
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM roles_permissions
        WHERE role_id = (SELECT id FROM roles WHERE name = 'owner')
        AND permission_id = (SELECT id FROM permissions WHERE name = 'brand')
        """
    )
