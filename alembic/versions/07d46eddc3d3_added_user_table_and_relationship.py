"""added user table and relationship

Revision ID: 07d46eddc3d3
Revises: 6c4972bbab84
Create Date: 2023-10-18 05:14:20.589662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07d46eddc3d3'
down_revision: Union[str, None] = '6c4972bbab84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)

    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_todo_user', 'users', ['user'], ['id'])
        batch_op.drop_column('owner')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner', sa.VARCHAR(), nullable=True))
        batch_op.drop_constraint('fk_todo_user', type_='foreignkey')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_id'))

    op.drop_table('users')
    # ### end Alembic commands ###