"""empty message

Revision ID: 3affb814f526
Revises: 795ec684c1b6
Create Date: 2025-05-23 01:01:17.083506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3affb814f526'
down_revision: Union[str, None] = '795ec684c1b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
