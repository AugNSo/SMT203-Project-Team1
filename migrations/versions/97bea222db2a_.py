"""empty message

Revision ID: 97bea222db2a
Revises: 60482f212282
Create Date: 2019-03-17 10:44:55.842065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97bea222db2a'
down_revision = '60482f212282'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cid', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('school', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('professor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('prof_course',
    sa.Column('cname', sa.String(length=80), nullable=False),
    sa.Column('pname', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['cname'], ['course.name'], ),
    sa.ForeignKeyConstraint(['pname'], ['professor.name'], ),
    sa.PrimaryKeyConstraint('cname', 'pname', name='prof_course_pk')
    )
    op.create_table('review',
    sa.Column('reviewer', sa.String(length=80), nullable=False),
    sa.Column('pname', sa.String(length=80), nullable=False),
    sa.Column('cname', sa.String(length=80), nullable=False),
    sa.Column('score1', sa.Float(), nullable=False),
    sa.Column('score2', sa.Float(), nullable=False),
    sa.Column('score3', sa.Float(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('school', sa.String(length=10), nullable=True),
    sa.Column('comment', sa.String(length=300), nullable=True),
    sa.Column('advice', sa.String(length=300), nullable=True),
    sa.ForeignKeyConstraint(['pname', 'cname'], ['prof_course.pname', 'prof_course.cname'], ),
    sa.PrimaryKeyConstraint('reviewer', 'pname', 'cname')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('prof_course')
    op.drop_table('professor')
    op.drop_table('course')
    # ### end Alembic commands ###
