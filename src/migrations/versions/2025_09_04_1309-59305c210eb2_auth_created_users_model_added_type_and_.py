"""auth: created users model + added type and owner for token

Revision ID: 59305c210eb2
Revises: 27240a0aed87
Create Date: 2025-09-04 13:09:31.752367

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "59305c210eb2"
down_revision: Union[str, Sequence[str], None] = "27240a0aed87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("birth_date", sa.DateTime(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.add_column("tokens", sa.Column("owner_id", sa.Integer(), nullable=False))
    tokentype_enum = postgresql.ENUM("ACCESS", "REFRESH", name="tokentype")
    tokentype_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "tokens",
        sa.Column(
            "type",
            tokentype_enum,
            nullable=False,
        ),
    )
    op.create_foreign_key(
        op.f("fk_tokens_owner_id_users"),
        "tokens",
        "users",
        ["owner_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("fk_tokens_owner_id_users"), "tokens", type_="foreignkey")
    op.drop_column("tokens", "type")
    op.drop_column("tokens", "owner_id")
    op.drop_table("users")
