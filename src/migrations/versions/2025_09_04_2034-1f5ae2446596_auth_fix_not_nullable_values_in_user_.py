"""auth: fix not-nullable values in User table

Revision ID: 1f5ae2446596
Revises: f9baadf337da
Create Date: 2025-09-04 20:34:38.170955

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1f5ae2446596"
down_revision: Union[str, Sequence[str], None] = "f9baadf337da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "first_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("users", "last_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "users",
        "birth_date",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
    op.alter_column("users", "email", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users", "email", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        "users",
        "birth_date",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )
    op.alter_column("users", "last_name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("users", "first_name", existing_type=sa.VARCHAR(), nullable=False)
