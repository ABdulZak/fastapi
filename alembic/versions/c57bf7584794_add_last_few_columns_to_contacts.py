"""add last few columns to contacts

Revision ID: c57bf7584794
Revises: 268f5a057152
Create Date: 2023-01-24 16:34:51.953483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c57bf7584794'
down_revision = '268f5a057152'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('contacts','title')
    op.drop_column('contacts', 'content')
    op.add_column('contacts', sa.Column('name', sa.String(), nullable = False))
    op.add_column('contacts', sa.Column('contact', sa.String(), nullable = False))
    op.add_column('contacts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('contacts', 'name')
    op.drop_column('contacts', 'contact')
    op.drop_column('contacts', 'created_at')
    op.add_column('contacts', sa.Column('title', sa.String(), nullable = False))
    op.add_column('contacts', sa.Column('content', sa.String(), nullable = False))
    pass
