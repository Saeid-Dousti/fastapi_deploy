"""add foreign-key to posts table

Revision ID: 6329ec467789
Revises: 6a80745c2410
Create Date: 2022-10-08 14:05:24.687207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6329ec467789'
down_revision = '6a80745c2410'
branch_labels = None
depends_on = None

#* 11:04
def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_coumn('posts', 'owner_id')
