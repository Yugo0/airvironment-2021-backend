"""add created column

Revision ID: 17ba7daa1797
Revises: be152219b1fe
Create Date: 2021-07-13 14:40:48.206158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17ba7daa1797'
down_revision = 'be152219b1fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('measurements', sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('measurements', 'created')
    # ### end Alembic commands ###