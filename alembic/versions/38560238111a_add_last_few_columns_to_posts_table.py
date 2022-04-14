"""add last few columns to posts table

Revision ID: 38560238111a
Revises: 662018c7e40e
Create Date: 2022-04-14 15:16:03.707298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38560238111a'
down_revision = '662018c7e40e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', 
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    
    op.add_column('posts', 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
