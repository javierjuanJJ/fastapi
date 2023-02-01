"""add content column to post table

Revision ID: ecfda23488fd
Revises: 6eac4e90d405
Create Date: 2023-02-01 16:49:57.929451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecfda23488fd'
down_revision = '6eac4e90d405'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
