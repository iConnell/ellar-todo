"""add column 'owner' to Todo table

Revision ID: f3c7b683be74
Revises: 844ca1a11017
Create Date: 2023-10-05 05:42:46.708398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3c7b683be74"
down_revision: Union[str, None] = "844ca1a11017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("owner", sa.String(20), nullable=True))


def downgrade() -> None:
    pass
