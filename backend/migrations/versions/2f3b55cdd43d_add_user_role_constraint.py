
"""add user role constraint

Revision ID: 2f3b55cdd43d
Revises: 8c4eb5fdc91a
Create Date: 2026-11-11 14:17:03.524455

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '2f3b55cdd43d'
down_revision: Union[str, Sequence[str], None] = '8c4eb5fdc91a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add a constraint allowing only valid user roles."""

    op.create_check_constraint(
        'ck_users_role',
        'users',
        "role IN ('user', 'admin')"
    )


def downgrade() -> None:
    """Remove the user role constraint."""

    op.drop_constraint(
        'ck_users_role',
        'users',
        type_='check'
    )
