"""renamed todo.user and set field as non nullable

Revision ID: 2e15552467b0
Revises: 488ad61db612
Create Date: 2023-10-18 05:16:42.603512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e15552467b0'
down_revision: Union[str, None] = '488ad61db612'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner', sa.Integer(), nullable=False))
        batch_op.drop_constraint('fk_todo_user', type_='foreignkey')
        batch_op.create_foreign_key('fk_todo_owner', 'users', ['owner'], ['id'])
        batch_op.drop_column('user')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint('fk_todo_owner', type_='foreignkey')
        batch_op.create_foreign_key('fk_todo_user', 'users', ['user'], ['id'])
        batch_op.drop_column('owner')

    # ### end Alembic commands ###
