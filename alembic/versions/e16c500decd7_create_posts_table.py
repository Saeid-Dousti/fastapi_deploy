"""create posts table

Revision ID: e16c500decd7
Revises: 
Create Date: 2022-10-08 09:39:30.976148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e16c500decd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',  sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title',  sa.String(), nullable=False)) #* 10:49


def downgrade() -> None:
    op.drop_table('posts') #* 10:49
