"""Created content table

Revision ID: af7fc35791e3
Revises: 5671cab461f1
Create Date: 2023-01-23 16:19:01.986913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af7fc35791e3'
down_revision = '5671cab461f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
                'contacts',
                 sa.Column('content', sa.String(), nullable=False)
                 )
    pass


def downgrade() -> None:
    op.drop_column('contacts', 'content')
    pass
