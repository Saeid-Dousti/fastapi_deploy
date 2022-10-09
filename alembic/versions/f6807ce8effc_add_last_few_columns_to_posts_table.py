"""add last few columns to posts table

Revision ID: f6807ce8effc
Revises: 6329ec467789
Create Date: 2022-10-08 14:17:36.372381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6807ce8effc'
down_revision = '6329ec467789'
branch_labels = None
depends_on = None

#* 11:06
def upgrade() -> None:
    op.add_column('posts', sa.Column(
                    'published', sa.Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column('posts', sa.Column(
                    'created_at', sa.TIMESTAMP(timezone=True), 
                    nullable=False, server_default=sa.text('now()')), )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
