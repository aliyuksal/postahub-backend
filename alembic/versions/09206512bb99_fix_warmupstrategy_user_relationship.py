"""Fix WarmupStrategy-User relationship

Revision ID: 09206512bb99
Revises: 8378cb7692e6
Create Date: 2025-05-23 00:33:48.291043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09206512bb99'
down_revision: Union[str, None] = '8378cb7692e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
