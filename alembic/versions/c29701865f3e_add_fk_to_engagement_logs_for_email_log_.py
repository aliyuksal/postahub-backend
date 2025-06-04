"""Add FK to engagement_logs for email_log_id

Revision ID: c29701865f3e
Revises: 8682ecdecac3
Create Date: 2025-05-25 22:12:32.054662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c29701865f3e'
down_revision: Union[str, None] = '8682ecdecac3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ Sadece foreign key ekleniyor, sütunlar zaten mevcut
    op.create_foreign_key(
        'fk_engagement_logs_email_log_id',
        'engagement_logs',
        'email_logs',
        ['email_log_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('fk_engagement_logs_email_log_id', 'engagement_logs', type_='foreignkey')
