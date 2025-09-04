"""auth: forgot to add unique constraint fot username

Revision ID: f9baadf337da
Revises: 59305c210eb2
Create Date: 2025-09-04 13:37:52.854714

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9baadf337da"
down_revision: Union[str, Sequence[str], None] = "59305c210eb2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(op.f("uq_users_username"), "users", ["username"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_users_username"), "users", type_="unique")
