"""create users table

Revision ID: dbcc5a6eddee
Revises: d31f92c19ffa
Create Date: 2022-04-14 14:29:36.594841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbcc5a6eddee'
down_revision = 'd31f92c19ffa'
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
