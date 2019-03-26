"""empty message

Revision ID: 70571ae44feb
Revises: ba618b8c67a2
Create Date: 2019-03-16 23:08:47.470670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70571ae44feb'
down_revision = 'ba618b8c67a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'id')
    # ### end Alembic commands ###