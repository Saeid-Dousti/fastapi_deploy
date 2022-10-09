"""add user table

Revision ID: 6a80745c2410
Revises: 8ca04ff04fb1
Create Date: 2022-10-08 12:07:46.679501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a80745c2410'
down_revision = '8ca04ff04fb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('create_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

def downgrade() -> None:
    op.drop_table('users')
