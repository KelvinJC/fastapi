"""add content column to posts table

Revision ID: d31f92c19ffa
Revises: 0acf93ddf6bb
Create Date: 2022-04-14 14:19:36.831644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd31f92c19ffa'
down_revision = '0acf93ddf6bb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
