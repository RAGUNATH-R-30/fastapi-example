"""add foreign key to post table

Revision ID: d7ddcf77a547
Revises: 98e092bbd1e2
Create Date: 2023-11-30 14:45:23.770023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7ddcf77a547'
down_revision: Union[str, None] = '98e092bbd1e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_user_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")

    pass


def downgrade() -> None:
    op.drop_constraint('posts_user_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
