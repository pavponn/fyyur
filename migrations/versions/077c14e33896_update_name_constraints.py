"""Update name constraints

Revision ID: 077c14e33896
Revises: cea7c979ff77
Create Date: 2020-08-23 11:56:40.927736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '077c14e33896'
down_revision = 'cea7c979ff77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
