"""add users table

Revision ID: 4c5331037964
Revises: af7fc35791e3
Create Date: 2023-01-24 15:32:49.513946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c5331037964'
down_revision = 'af7fc35791e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
                    'users', 
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
