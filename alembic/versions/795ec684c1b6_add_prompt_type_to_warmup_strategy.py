"""Add prompt_type to warmup_strategy

Revision ID: 795ec684c1b6
Revises: 163a495a4c16
Create Date: 2025-05-23 00:52:12.586152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '795ec684c1b6'
down_revision: Union[str, None] = '163a495a4c16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('warmup_strategies', sa.Column('prompt_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('warmup_strategies', 'prompt_type')
    # ### end Alembic commands ###
