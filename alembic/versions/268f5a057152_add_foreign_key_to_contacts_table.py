"""add foreign-key to contacts table

Revision ID: 268f5a057152
Revises: 4c5331037964
Create Date: 2023-01-24 16:22:20.753116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '268f5a057152'
down_revision = '4c5331037964'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('contacts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('contact_users_fk', source_table='contacts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('contact_users_fk', table_name='contacts')
    op.drop_column('contacts', 'owner_id')
    pass
