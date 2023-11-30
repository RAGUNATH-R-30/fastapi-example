"""create users table

Revision ID: 98e092bbd1e2
Revises: 1950ec5dc664
Create Date: 2023-11-30 14:16:09.696879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98e092bbd1e2'
down_revision: Union[str, None] = '1950ec5dc664'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
