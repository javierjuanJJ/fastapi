"""create post table

Revision ID: 6eac4e90d405
Revises: 060f6283176a
Create Date: 2023-02-01 16:43:22.952698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eac4e90d405'
down_revision = '060f6283176a'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

