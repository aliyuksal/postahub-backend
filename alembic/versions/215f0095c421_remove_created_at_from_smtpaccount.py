"""Remove created_at from SMTPAccount

Revision ID: 215f0095c421
Revises: 497d5f596c0f
Create Date: 2025-05-23 02:15:00.698425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '215f0095c421'
down_revision: Union[str, None] = '497d5f596c0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column('smtp_accounts', 'created_at')
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
