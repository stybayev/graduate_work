"""New Migration

Revision ID: 70a851e24518
Revises:
Create Date: 2024-06-26 07:17:05.290024

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
import uuid

# revision identifiers, used by Alembic.
revision: str = "4df764df8196"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create schema
    op.execute('CREATE SCHEMA IF NOT EXISTS profiles_service')

    # Create table
    op.create_table(
        'profiles',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('phone_number', sa.String(length=15), nullable=False, unique=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        schema='profiles_service'
    )


def downgrade():
    # Drop table
    op.drop_table('profiles', schema='profiles_service')

    # Drop schema
    op.execute('DROP SCHEMA IF EXISTS profiles_service CASCADE')
