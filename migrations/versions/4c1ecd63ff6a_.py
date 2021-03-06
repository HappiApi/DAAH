"""empty message

Revision ID: 4c1ecd63ff6a
Revises: 59d51fc04fe0
Create Date: 2015-11-04 12:13:31.171325

"""

# revision identifiers, used by Alembic.
revision = '4c1ecd63ff6a'
down_revision = '59d51fc04fe0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['list_id'], ['list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'user', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column(u'user', sa.Column('username', sa.String(), nullable=True))
    op.drop_column(u'user', 'url')
    op.drop_column(u'user', 'result_all')
    op.drop_column(u'user', 'result_no_stop_words')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'user', sa.Column('result_no_stop_words', postgresql.JSON(), autoincrement=False, nullable=True))
    op.add_column(u'user', sa.Column('result_all', postgresql.JSON(), autoincrement=False, nullable=True))
    op.add_column(u'user', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column(u'user', 'username')
    op.drop_column(u'user', 'hashed_password')
    op.drop_table('item')
    op.drop_table('list')
    ### end Alembic commands ###
