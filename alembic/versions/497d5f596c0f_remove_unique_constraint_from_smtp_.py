"""Remove unique constraint from smtp_accounts.email

Revision ID: 497d5f596c0f
Revises: 3243cc62e236
Create Date: 2025-05-23 02:05:38.984276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '497d5f596c0f'
down_revision: Union[str, None] = '3243cc62e236'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('smtp_accounts_email_key', 'smtp_accounts', type_='unique')

    pass


def downgrade() -> None:
    pass
