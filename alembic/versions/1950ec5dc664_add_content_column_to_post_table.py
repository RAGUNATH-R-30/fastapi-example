"""add content column to post table

Revision ID: 1950ec5dc664
Revises: 0b57c0ae2782
Create Date: 2023-11-30 13:29:56.570091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1950ec5dc664'
down_revision: Union[str, None] = '0b57c0ae2782'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
