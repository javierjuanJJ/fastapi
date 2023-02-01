"""add user table

Revision ID: 60681508b819
Revises: ecfda23488fd
Create Date: 2023-02-01 16:55:15.020006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60681508b819'
down_revision = 'ecfda23488fd'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
