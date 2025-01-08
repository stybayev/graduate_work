"""New Migration

Revision ID: 70a851e24518
Revises:
Create Date: 2024-06-26 07:17:05.290024

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3df764df8196"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")
    op.execute("CREATE SCHEMA IF NOT EXISTS partman")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_partman SCHEMA partman")

    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("permissions", sa.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="auth",
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("login", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=True),
        sa.Column("last_name", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_staff', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("login"),
        sa.UniqueConstraint("email"),
        schema="auth",
    )

    op.create_table(
        "login_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("login_time", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "login_time"),
        sa.UniqueConstraint("id", "login_time"),
        postgresql_partition_by="RANGE (login_time)",
        schema="auth",
    )
    op.execute(
        """SELECT partman.create_parent(
            'auth.login_history',p_control := 'login_time',p_type := 'native',p_interval := 'monthly',p_premake := 2
        ) """,
    )
    op.execute(
        """UPDATE partman.part_config SET retention = '12 month', retention_keep_table=false
        WHERE parent_table = 'auth.login_history'""",
    )

    op.create_table(
        "user_roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["auth.roles.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"]),
        sa.PrimaryKeyConstraint("id", "user_id", "role_id"),
        sa.UniqueConstraint("id"),
        schema="auth",
    )

    op.create_table(
        "social_account",
        sa.Column("id", sa.UUID(), nullable=False, default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("social_id", sa.Text(), nullable=False),
        sa.Column("social_name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("social_id", "social_name", name="social_pk"),
        schema="auth",
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("social_account", schema="auth")
    op.drop_table("user_roles", schema="auth")
    op.drop_table("login_history", schema="auth")
    op.drop_table("users", schema="auth")
    op.drop_table("roles", schema="auth")
    # ### end Alembic commands ###
