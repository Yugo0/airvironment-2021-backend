"""Add table measurements to db

Revision ID: be152219b1fe
Revises: 
Create Date: 2021-07-13 12:42:03.295279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be152219b1fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('measurements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('humidity', sa.Float(), nullable=False),
    sa.Column('pollution', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###




def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('measurements')
    # ### end Alembic commands ###
