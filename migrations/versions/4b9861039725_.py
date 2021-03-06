"""empty message

Revision ID: 4b9861039725
Revises: 
Create Date: 2018-10-30 21:06:30.581107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b9861039725'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('boss',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('signal', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recruit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('unit', sa.String(length=100), nullable=True),
    sa.Column('content', sa.String(length=100), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('pay', sa.String(length=100), nullable=True),
    sa.Column('commend', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('contact', sa.String(length=100), nullable=True),
    sa.Column('remark', sa.String(length=1000), nullable=True),
    sa.Column('hasMoveIn', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tenement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('flat_name', sa.String(length=50), nullable=False),
    sa.Column('flat_id', sa.String(length=50), nullable=True),
    sa.Column('room_count', sa.Integer(), nullable=False),
    sa.Column('bathroom_count', sa.Integer(), nullable=False),
    sa.Column('kitchen_count', sa.Integer(), nullable=True),
    sa.Column('livingroom_count', sa.Integer(), nullable=True),
    sa.Column('price', sa.String(length=50), nullable=False),
    sa.Column('deposit', sa.Integer(), nullable=False),
    sa.Column('telephone1', sa.String(length=50), nullable=False),
    sa.Column('telephone2', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('kitchen', sa.String(length=50), nullable=False),
    sa.Column('window', sa.String(length=50), nullable=False),
    sa.Column('lift', sa.String(length=50), nullable=False),
    sa.Column('remark', sa.String(length=1000), nullable=True),
    sa.Column('hasMoveIn', sa.Boolean(), nullable=False),
    sa.Column('image1', sa.String(length=200), nullable=True),
    sa.Column('image2', sa.String(length=200), nullable=True),
    sa.Column('image3', sa.String(length=200), nullable=True),
    sa.Column('image4', sa.String(length=200), nullable=True),
    sa.Column('image5', sa.String(length=200), nullable=True),
    sa.Column('image6', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('tenement')
    op.drop_table('recruit')
    op.drop_table('boss')
    # ### end Alembic commands ###
