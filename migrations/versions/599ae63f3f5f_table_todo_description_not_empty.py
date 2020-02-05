"""table todo description not empty

Revision ID: 599ae63f3f5f
Revises: 71caa97f2922
Create Date: 2020-02-05 15:10:35.104485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '599ae63f3f5f'
down_revision = '71caa97f2922'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("todos") as batch_op:
        batch_op.drop_column('description')
        batch_op.add_column(sa.Column('description', sa.TEXT, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###
