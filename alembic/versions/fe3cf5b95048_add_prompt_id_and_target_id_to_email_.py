"""Add prompt_id and target_id to email_logs

Revision ID: fe3cf5b95048
Revises: 215f0095c421
Create Date: 2025-05-23 03:17:23.880414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe3cf5b95048'
down_revision: Union[str, None] = '215f0095c421'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('email_logs', sa.Column('prompt_id', sa.Integer(), nullable=True))
    op.add_column('email_logs', sa.Column('target_id', sa.Integer(), nullable=True))

    op.create_foreign_key(
        "fk_email_logs_prompt_id", "email_logs", "ai_prompts", ["prompt_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_email_logs_target_id", "email_logs", "warmup_targets", ["target_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_email_logs_prompt_id", "email_logs", type_="foreignkey")
    op.drop_constraint("fk_email_logs_target_id", "email_logs", type_="foreignkey")

    op.drop_column('email_logs', 'prompt_id')
    op.drop_column('email_logs', 'target_id')
