"""add content column to posts table

Revision ID: 8ca04ff04fb1
Revises: e16c500decd7
Create Date: 2022-10-08 11:48:41.426262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ca04ff04fb1'
down_revision = 'e16c500decd7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
