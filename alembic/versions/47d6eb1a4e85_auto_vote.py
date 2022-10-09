"""auto-vote

Revision ID: 47d6eb1a4e85
Revises: f6807ce8effc
Create Date: 2022-10-08 19:31:31.505968

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '47d6eb1a4e85'
down_revision = 'f6807ce8effc'
branch_labels = None
depends_on = None

#* 11:11
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.alter_column('posts', 'published',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('true'))
    op.add_column('users', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.drop_column('users', 'create_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
